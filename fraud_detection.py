"""
Fraud detection using Isolation Forest for abnormal transactions.
"""
import numpy as np
from sklearn.ensemble import IsolationForest


class FraudDetector:
    """Identify fake transactions, suspicious spending, abnormal behavior."""

    def analyze(self, transactions: list[dict]) -> list[dict]:
        if not transactions:
            return []

        amounts = np.array([[t["amount"]] for t in transactions])
        model = IsolationForest(contamination=0.15, random_state=42)
        predictions = model.fit_predict(amounts)
        scores = model.decision_function(amounts)

        results = []
        for i, txn in enumerate(transactions):
            is_anomaly = predictions[i] == -1
            score = float(scores[i])
            if txn.get("is_fraud"):
                label = "Fake Transaction"
            elif is_anomaly:
                label = "Suspicious Spending"
            else:
                label = "Normal"
            results.append({
                **txn,
                "fraud_label": label,
                "fraud_score": round(abs(score), 3),
                "is_flagged": is_anomaly or txn.get("is_fraud", False),
            })
        return results

    def summary_counts(self, analyzed: list[dict]) -> dict:
        counts = {"Normal": 0, "Suspicious Spending": 0, "Fake Transaction": 0}
        for row in analyzed:
            label = row.get("fraud_label", "Normal")
            counts[label] = counts.get(label, 0) + 1
        return counts
