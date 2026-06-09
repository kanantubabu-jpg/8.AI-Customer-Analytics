"""
Collaborative Filtering, Matrix Factorization (NMF), and Hybrid Recommender.
"""
import numpy as np
import pandas as pd
from sklearn.decomposition import NMF


class CollaborativeRecommender:
    """User-item matrix recommenders."""

    PRODUCTS = ["Electronics", "Clothing", "Home", "Sports", "Beauty"]

    def _build_matrix(self, journeys: list) -> tuple[pd.DataFrame, list, list]:
        rows = []
        for j in journeys:
            if j.event_type in ("purchase", "add_to_cart", "view_product"):
                product = j.product_id or "General"
                weight = {"purchase": 3, "add_to_cart": 2, "view_product": 1}.get(j.event_type, 1)
                rows.append({"customer_id": j.customer_id, "product": product, "score": weight})
        if not rows:
            return pd.DataFrame(), [], []
        df = pd.DataFrame(rows)
        matrix = df.pivot_table(
            index="customer_id", columns="product", values="score", aggfunc="sum", fill_value=0
        )
        return matrix, list(matrix.index), list(matrix.columns)

    def collaborative_filtering(self, journeys: list, top_n: int = 5) -> dict:
        matrix, users, products = self._build_matrix(journeys)
        if matrix.empty:
            return {"labels": self.PRODUCTS[:top_n], "scores": [0.5] * min(top_n, len(self.PRODUCTS))}
        scores = matrix.sum(axis=0).sort_values(ascending=False).head(top_n)
        return {"labels": list(scores.index), "scores": [round(float(v), 2) for v in scores.values]}

    def matrix_factorization(self, journeys: list, n_components: int = 3) -> dict:
        matrix, users, products = self._build_matrix(journeys)
        if matrix.empty or matrix.shape[0] < 2:
            return {"labels": ["Factor 1", "Factor 2", "Factor 3"], "scores": [1.0, 0.8, 0.6]}
        n_comp = min(n_components, matrix.shape[0], matrix.shape[1])
        model = NMF(n_components=n_comp, random_state=42, max_iter=500)
        w = model.fit_transform(matrix.values)
        factor_strength = w.sum(axis=0)
        labels = [f"Latent Factor {i+1}" for i in range(n_comp)]
        return {"labels": labels, "scores": [round(float(s), 2) for s in factor_strength]}

    def hybrid_recommender(self, journeys: list, segment_products: dict, top_n: int = 5) -> dict:
        cf = self.collaborative_filtering(journeys, top_n=top_n)
        content_labels = list(segment_products.keys())[:top_n]
        content_scores = [segment_products.get(l, 0.5) for l in content_labels]
        all_labels = list(dict.fromkeys(cf["labels"] + content_labels))[:top_n]
        hybrid_scores = []
        for label in all_labels:
            cf_idx = cf["labels"].index(label) if label in cf["labels"] else -1
            cf_score = cf["scores"][cf_idx] if cf_idx >= 0 else 0
            ct_score = segment_products.get(label, 0)
            hybrid_scores.append(round(cf_score * 0.6 + ct_score * 0.4, 2))
        return {"labels": all_labels, "cf": [cf["scores"][cf["labels"].index(l)] if l in cf["labels"] else 0 for l in all_labels],
                "content": [segment_products.get(l, 0) for l in all_labels],
                "hybrid": hybrid_scores}
