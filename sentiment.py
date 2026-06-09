"""
Customer review sentiment analysis using TextBlob.
"""
from textblob import TextBlob


class SentimentAnalyzer:
    """Classify review text as Positive, Negative, or Neutral."""

    def analyze(self, text: str) -> dict:
        """
        Analyze sentiment of review text.
        Returns polarity score (-1 to 1) and classification label.
        """
        if not text or not text.strip():
            return {"sentiment": "Neutral", "score": 0.0, "insight": "No text provided."}

        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        if polarity > 0.1:
            sentiment = "Positive"
            insight = "Customer expresses satisfaction and positive experience."
        elif polarity < -0.1:
            sentiment = "Negative"
            insight = "Customer reports dissatisfaction; follow-up recommended."
        else:
            sentiment = "Neutral"
            insight = "Mixed or neutral feedback; monitor for trends."

        return {
            "sentiment": sentiment,
            "score": round(polarity, 3),
            "insight": insight,
        }

    def analyze_batch(self, reviews: list[str]) -> list[dict]:
        """Analyze multiple reviews."""
        return [self.analyze(review) for review in reviews]
