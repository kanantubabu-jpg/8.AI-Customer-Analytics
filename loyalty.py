"""
Loyalty score: Purchase Frequency + Average Spending + Review Sentiment
"""


class LoyaltyCalculator:
    """Compute loyalty score (0–100) per customer."""

    def _sentiment_component(self, scores: list[float]) -> float:
        if not scores:
            return 16.67
        avg = sum(scores) / len(scores)
        normalized = (avg + 1) / 2
        return round(normalized * 33.34, 2)

    def compute(
        self,
        total_purchases: int,
        spending_score: int,
        sentiment_scores: list[float] | None = None,
    ) -> dict:
        freq = min(total_purchases / 20.0, 1.0) * 33.33
        spending = min(spending_score / 100.0, 1.0) * 33.33
        sentiment = self._sentiment_component(sentiment_scores or [])
        total = round(freq + spending + sentiment, 2)
        return {
            "loyalty_score": total,
            "purchase_frequency": round(freq, 2),
            "average_spending": round(spending, 2),
            "review_sentiment": round(sentiment, 2),
        }
