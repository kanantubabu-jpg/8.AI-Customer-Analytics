"""
Central analytics service for all advanced module charts.
"""
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import random

from sqlalchemy import func

from campaign_analytics import CampaignAnalytics
from collaborative_recommender import CollaborativeRecommender
from database import (
    Customer,
    CustomerJourney,
    EmailCampaign,
    LiveActivity,
    Review,
    Transaction,
    db,
)
from fraud_detection import FraudDetector
from loyalty import LoyaltyCalculator
from predictor import PredictionService


class AnalyticsService:
    """Generate chart data for each analytics module."""

    def __init__(self):
        self.predictor = PredictionService()
        self.loyalty_calc = LoyaltyCalculator()
        self.fraud_detector = FraudDetector()
        self.campaign = CampaignAnalytics()
        self.cf_recommender = CollaborativeRecommender()

    def _customer_sentiments(self) -> dict[str, list[float]]:
        mapping: dict[str, list[float]] = defaultdict(list)
        for r in Review.query.all():
            if r.customer_id and r.sentiment_score is not None:
                mapping[r.customer_id].append(r.sentiment_score)
        return mapping

    def update_customer_scores(self, force: bool = False) -> None:
        sentiments = self._customer_sentiments()
        updated = False
        for c in Customer.query.all():
            if force or not c.predicted_clv:
                try:
                    pred = self.predictor.predict_all(c.age, c.income, c.spending_score)
                    c.predicted_clv = pred["clv"]
                    c.segment = pred["segment"]
                    updated = True
                except Exception:
                    c.predicted_clv = c.clv or 0
            loyalty = self.loyalty_calc.compute(
                c.total_purchases, c.spending_score, sentiments.get(c.customer_id, [])
            )
            c.loyalty_score = loyalty["loyalty_score"]
        if updated:
            db.session.commit()
        else:
            db.session.commit()

    def predicted_clv_chart(self) -> dict:
        customers = Customer.query.order_by(Customer.predicted_clv.desc()).limit(10).all()
        if not customers or not customers[0].predicted_clv:
            self.update_customer_scores()
            customers = Customer.query.order_by(Customer.predicted_clv.desc()).limit(10).all()
        return {
            "labels": [c.customer_id for c in customers],
            "values": [round(c.predicted_clv or c.clv, 0) for c in customers],
        }

    def email_campaign_chart(self) -> dict:
        campaigns = EmailCampaign.query.all()
        return self.campaign.campaign_tracking_chart(campaigns)

    def campaign_roi_chart(self) -> dict:
        campaigns = EmailCampaign.query.all()
        return self.campaign.roi_chart(campaigns)

    def best_targets_chart(self) -> dict:
        self.update_customer_scores()
        customers = Customer.query.filter_by(churned=False).all()
        targets = []
        for c in customers:
            try:
                prob = self.predictor.predict_purchase(c.age, c.income, c.spending_score, c.total_purchases)
            except Exception:
                prob = 0.5
            score = prob * 0.5 + (c.loyalty_score / 100) * 0.3 + (c.predicted_clv or c.clv) / 15000 * 0.2
            targets.append((c.customer_id, round(score * 100, 1)))
        targets.sort(key=lambda x: x[1], reverse=True)
        top = targets[:10]
        return {"labels": [t[0] for t in top], "values": [t[1] for t in top]}

    def conversion_by_segment_chart(self) -> dict:
        self.update_customer_scores()
        segment_probs: dict[str, list[float]] = defaultdict(list)
        for c in Customer.query.all():
            seg = c.segment or "Unknown"
            try:
                prob = self.predictor.predict_purchase(c.age, c.income, c.spending_score, c.total_purchases)
            except Exception:
                prob = 0.5
            segment_probs[seg].append(prob * 100)
        labels = list(segment_probs.keys())
        values = [round(sum(v) / len(v), 1) for v in segment_probs.values()]
        return {"labels": labels, "values": values}

    def loyalty_chart(self) -> dict:
        sentiments = self._customer_sentiments()
        customers = Customer.query.limit(10).all()
        labels, freq, spend, sent, total = [], [], [], [], []
        for c in customers:
            l = self.loyalty_calc.compute(c.total_purchases, c.spending_score, sentiments.get(c.customer_id, []))
            labels.append(c.customer_id)
            freq.append(l["purchase_frequency"])
            spend.append(l["average_spending"])
            sent.append(l["review_sentiment"])
            total.append(l["loyalty_score"])
        return {"labels": labels, "frequency": freq, "spending": spend, "sentiment": sent, "total": total}

    def purchase_history_chart(self) -> dict:
        customers = Customer.query.order_by(Customer.total_purchases.desc()).limit(10).all()
        return {
            "labels": [c.customer_id for c in customers],
            "values": [c.total_purchases for c in customers],
        }

    def fraud_chart(self) -> dict:
        txns = Transaction.query.all()
        data = [{"amount": t.amount, "is_fraud": t.is_fraud, "customer_id": t.customer_id} for t in txns]
        analyzed = self.fraud_detector.analyze(data)
        counts = self.fraud_detector.summary_counts(analyzed)
        return {"labels": list(counts.keys()), "values": list(counts.values())}

    def journey_funnel_chart(self) -> dict:
        stages = ["visit", "view_product", "add_to_cart", "purchase"]
        counts = []
        for stage in stages:
            counts.append(CustomerJourney.query.filter_by(event_type=stage).count())
        return {"labels": ["Visit", "View Product", "Add To Cart", "Purchase"], "values": counts}

    def live_sales_chart(self) -> dict:
        self._seed_live_activity()
        recent = (
            LiveActivity.query.filter(LiveActivity.activity_type == "sale")
            .order_by(LiveActivity.created_at.desc())
            .limit(12)
            .all()
        )
        recent = list(reversed(recent))
        return {
            "labels": [a.created_at.strftime("%H:%M:%S") for a in recent],
            "values": [a.value for a in recent],
        }

    def live_activity_chart(self) -> dict:
        self._seed_live_activity()
        types = ["browse", "cart", "purchase", "review"]
        values = []
        for t in types:
            values.append(
                LiveActivity.query.filter(
                    LiveActivity.activity_type == t,
                    LiveActivity.created_at >= datetime.utcnow() - timedelta(minutes=30),
                ).count()
            )
        return {"labels": ["Browse", "Add Cart", "Purchase", "Review"], "values": values}

    def collaborative_filtering_chart(self) -> dict:
        journeys = CustomerJourney.query.all()
        return self.cf_recommender.collaborative_filtering(journeys)

    def matrix_factorization_chart(self) -> dict:
        journeys = CustomerJourney.query.all()
        return self.cf_recommender.matrix_factorization(journeys)

    def hybrid_recommender_chart(self) -> dict:
        journeys = CustomerJourney.query.all()
        seg_products = {"Electronics": 0.9, "Clothing": 0.7, "Home": 0.6, "Sports": 0.8, "Beauty": 0.5}
        return self.cf_recommender.hybrid_recommender(journeys, seg_products)

    def _seed_live_activity(self) -> None:
        if LiveActivity.query.count() > 50:
            return
        types = ["sale", "browse", "cart", "purchase", "review"]
        for i in range(20):
            db.session.add(
                LiveActivity(
                    customer_id=f"C{random.randint(1, 50):03d}",
                    activity_type=random.choice(types),
                    value=round(random.uniform(500, 5000), 2),
                )
            )
        db.session.commit()
