"""
Train and persist ML models for customer analytics.
Run: python train_model.py
"""
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from config import Config

SEGMENT_LABELS = {
    0: "Budget Conscious",
    1: "Standard Shoppers",
    2: "Premium Loyalists",
    3: "High-Value Champions",
}


class ModelTrainer:
    """Train segmentation, classification, and regression models."""

    def __init__(self, dataset_dir: str | None = None, models_dir: str | None = None):
        self.dataset_dir = dataset_dir or Config.DATASET_DIR
        self.models_dir = models_dir or Config.MODELS_DIR
        os.makedirs(self.models_dir, exist_ok=True)

    def load_customers(self) -> pd.DataFrame:
        path = os.path.join(self.dataset_dir, "customers.csv")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Customer dataset not found: {path}")
        return pd.read_csv(path)

    def load_sales(self) -> pd.DataFrame:
        path = os.path.join(self.dataset_dir, "sales.csv")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Sales dataset not found: {path}")
        return pd.read_csv(path)

    def train_segmentation(self, df: pd.DataFrame) -> dict:
        """K-Means clustering on age, income, spending_score."""
        features = df[["age", "income", "spending_score"]].values
        scaler = StandardScaler()
        scaled = scaler.fit_transform(features)

        kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        kmeans.fit(scaled)

        bundle = {"model": kmeans, "scaler": scaler, "labels": SEGMENT_LABELS}
        joblib.dump(bundle, os.path.join(self.models_dir, "segmentation.pkl"))
        return bundle

    def train_purchase_model(self, df: pd.DataFrame) -> RandomForestClassifier:
        """Random Forest for purchase prediction."""
        x = df[["age", "income", "spending_score", "total_purchases"]]
        y = df["will_purchase"]

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2, random_state=42
        )
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(x_train, y_train)
        score = model.score(x_test, y_test)
        print(f"Purchase model accuracy: {score:.2%}")

        joblib.dump(model, os.path.join(self.models_dir, "purchase.pkl"))
        return model

    def train_churn_model(self, df: pd.DataFrame) -> RandomForestClassifier:
        """Random Forest for churn prediction."""
        x = df[["age", "income", "spending_score", "total_purchases", "clv"]]
        y = df["churned"]

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2, random_state=42
        )
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(x_train, y_train)
        score = model.score(x_test, y_test)
        print(f"Churn model accuracy: {score:.2%}")

        joblib.dump(model, os.path.join(self.models_dir, "churn.pkl"))
        return model

    def train_clv_model(self, df: pd.DataFrame) -> LinearRegression:
        """Linear Regression for Customer Lifetime Value."""
        x = df[["age", "income", "spending_score", "total_purchases"]]
        y = df["clv"]

        model = LinearRegression()
        model.fit(x, y)
        score = model.score(x, y)
        print(f"CLV model R² score: {score:.2%}")

        joblib.dump(model, os.path.join(self.models_dir, "clv.pkl"))
        return model

    def train_sales_forecast(self, df: pd.DataFrame) -> dict:
        """Linear regression on monthly sales index for revenue forecast."""
        df = df.copy()
        df["period"] = range(1, len(df) + 1)
        x = df[["period"]].values
        y = df["revenue"].values

        model = LinearRegression()
        model.fit(x, y)

        bundle = {
            "model": model,
            "last_period": len(df),
            "historical": df[["month", "year", "revenue"]].to_dict("records"),
        }
        joblib.dump(bundle, os.path.join(self.models_dir, "sales_forecast.pkl"))
        return bundle

    def train_all(self) -> None:
        """Train all models and save to disk."""
        customers = self.load_customers()
        sales = self.load_sales()

        print("Training segmentation model (K-Means)...")
        self.train_segmentation(customers)

        print("Training purchase prediction model (Random Forest)...")
        self.train_purchase_model(customers)

        print("Training churn prediction model (Random Forest)...")
        self.train_churn_model(customers)

        print("Training CLV model (Linear Regression)...")
        self.train_clv_model(customers)

        print("Training sales forecast model...")
        self.train_sales_forecast(sales)

        print(f"All models saved to {self.models_dir}")


if __name__ == "__main__":
    ModelTrainer().train_all()
