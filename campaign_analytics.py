"""
Email campaign tracking and ROI prediction.
"""
from sklearn.linear_model import LinearRegression
import numpy as np


class CampaignAnalytics:
    """Track campaigns and predict ROI."""

    def campaign_tracking_chart(self, campaigns: list) -> dict:
        return {
            "labels": [c.campaign_name for c in campaigns],
            "sent": [c.emails_sent for c in campaigns],
            "opens": [c.opens for c in campaigns],
            "clicks": [c.clicks for c in campaigns],
            "conversions": [c.conversions for c in campaigns],
        }

    def roi_chart(self, campaigns: list) -> dict:
        labels, actual_roi, predicted_roi = [], [], []
        if len(campaigns) >= 3:
            x_train, y_train = [], []
            for c in campaigns[:-2]:
                rate = c.clicks / max(c.emails_sent, 1)
                x_train.append([rate, c.cost])
                y_train.append((c.revenue - c.cost) / max(c.cost, 1) * 100)
            model = LinearRegression()
            model.fit(np.array(x_train), np.array(y_train))
            for c in campaigns:
                rate = c.clicks / max(c.emails_sent, 1)
                pred = float(model.predict([[rate, c.cost]])[0])
                actual = (c.revenue - c.cost) / max(c.cost, 1) * 100
                labels.append(c.campaign_name)
                actual_roi.append(round(actual, 1))
                predicted_roi.append(round(pred, 1))
        else:
            for c in campaigns:
                labels.append(c.campaign_name)
                actual_roi.append(round((c.revenue - c.cost) / max(c.cost, 1) * 100, 1))
                predicted_roi.append(actual_roi[-1])
        return {"labels": labels, "actual": actual_roi, "predicted": predicted_roi}
