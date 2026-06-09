"""
ML prediction service loading trained models for inference.
"""
import os

import joblib
import numpy as np

from config import Config
from recommendation import RecommendationEngine


class PredictionService:
    """Load models and run customer analytics predictions."""

    def __init__(self, models_dir: str | None = None):
        self.models_dir = models_dir or Config.MODELS_DIR
        self.recommender = RecommendationEngine()
        self._models_loaded = False
        self.segmentation = None
        self.purchase = None
        self.churn = None
        self.clv = None
        self.sales_forecast = None

    def _load_model(self, name: str):
        path = os.path.join(self.models_dir, name)
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Model {name} not found. Run: python train_model.py"
            )
        return joblib.load(path)

    def load_models(self) -> None:
        """Load all persisted models from disk."""
        if self._models_loaded:
            return
        self.segmentation = self._load_model("segmentation.pkl")
        self.purchase = self._load_model("purchase.pkl")
        self.churn = self._load_model("churn.pkl")
        self.clv = self._load_model("clv.pkl")
        self.sales_forecast = self._load_model("sales_forecast.pkl")
        self._models_loaded = True

    def predict_segment(self, age: int, income: float, spending_score: int) -> str:
        """Predict customer segment using K-Means."""
        self.load_models()
        features = np.array([[age, income, spending_score]])
        scaled = self.segmentation["scaler"].transform(features)
        cluster = int(self.segmentation["model"].predict(scaled)[0])
        return self.segmentation["labels"].get(cluster, f"Segment {cluster}")

    def predict_purchase(
        self, age: int, income: float, spending_score: int, total_purchases: int = 5
    ) -> float:
        """Return purchase probability (0-1)."""
        self.load_models()
        features = np.array([[age, income, spending_score, total_purchases]])
        proba = self.purchase.predict_proba(features)[0]
        # Class 1 = will purchase
        purchase_class = 1 if 1 in self.purchase.classes_ else self.purchase.classes_[-1]
        idx = list(self.purchase.classes_).index(purchase_class)
        return float(proba[idx])

    def predict_churn(
        self,
        age: int,
        income: float,
        spending_score: int,
        total_purchases: int = 5,
        clv: float = 5000,
    ) -> float:
        """Return churn risk probability (0-1)."""
        self.load_models()
        features = np.array([[age, income, spending_score, total_purchases, clv]])
        proba = self.churn.predict_proba(features)[0]
        churn_class = 1 if 1 in self.churn.classes_ else self.churn.classes_[-1]
        idx = list(self.churn.classes_).index(churn_class)
        return float(proba[idx])

    def predict_clv(
        self, age: int, income: float, spending_score: int, total_purchases: int = 5
    ) -> float:
        """Predict Customer Lifetime Value."""
        self.load_models()
        features = np.array([[age, income, spending_score, total_purchases]])
        return float(self.clv.predict(features)[0])

    def predict_all(self, age: int, income: float, spending_score: int) -> dict:
        """Run full prediction pipeline."""
        clv = self.predict_clv(age, income, spending_score)
        segment = self.predict_segment(age, income, spending_score)
        purchase_prob = self.predict_purchase(age, income, spending_score)
        churn_risk = self.predict_churn(
            age, income, spending_score, clv=clv
        )
        recommendations = self.recommender.get_recommendations(segment)

        return {
            "age": age,
            "income": income,
            "spending_score": spending_score,
            "segment": segment,
            "purchase_probability": purchase_prob,
            "churn_risk": churn_risk,
            "clv": clv,
            "recommendations": recommendations,
        }

    def get_sales_forecast(self, months_ahead: int = 6) -> dict:
        """Generate future revenue forecast."""
        self.load_models()
        bundle = self.sales_forecast
        model = bundle["model"]
        last_period = bundle["last_period"]
        historical = bundle["historical"]

        future_labels = []
        future_revenue = []
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December",
        ]
        last_record = historical[-1]
        start_month_idx = month_names.index(last_record["month"])
        start_year = last_record["year"]

        for i in range(1, months_ahead + 1):
            period = last_period + i
            revenue = float(model.predict([[period]])[0])
            month_idx = (start_month_idx + i) % 12
            year = start_year + (start_month_idx + i) // 12
            future_labels.append(f"{month_names[month_idx][:3]} {year}")
            future_revenue.append(round(revenue, 2))

        return {
            "historical_labels": [
                f"{r['month'][:3]} {r['year']}" for r in historical
            ],
            "historical_revenue": [r["revenue"] for r in historical],
            "forecast_labels": future_labels,
            "forecast_revenue": future_revenue,
        }

    def get_segment_distribution(self) -> dict:
        """Return segment counts for pie chart from customer dataset."""
        import pandas as pd

        path = os.path.join(Config.DATASET_DIR, "customers.csv")
        if not os.path.exists(path):
            return {"labels": [], "values": []}

        df = pd.read_csv(path)
        self.load_models()
        segments = []
        for _, row in df.iterrows():
            seg = self.predict_segment(
                int(row["age"]), float(row["income"]), int(row["spending_score"])
            )
            segments.append(seg)

        from collections import Counter

        counts = Counter(segments)
        return {"labels": list(counts.keys()), "values": list(counts.values())}
