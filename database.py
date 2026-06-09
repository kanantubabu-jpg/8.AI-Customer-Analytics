"""
SQLAlchemy database models for the AI Customer Analytics platform.
"""
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Customer(db.Model):
    """Customer demographic and behavioral data."""

    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(50), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    income = db.Column(db.Float, nullable=False)
    spending_score = db.Column(db.Integer, nullable=False)
    segment = db.Column(db.String(50))
    total_purchases = db.Column(db.Integer, default=0)
    churned = db.Column(db.Boolean, default=False)
    clv = db.Column(db.Float, default=0.0)
    predicted_clv = db.Column(db.Float, default=0.0)
    loyalty_score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Sale(db.Model):
    """Monthly sales records."""

    __tablename__ = "sales"

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    revenue = db.Column(db.Float, nullable=False)
    units_sold = db.Column(db.Integer, default=0)
    product_category = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Review(db.Model):
    """Customer review with sentiment analysis results."""

    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(50))
    review_text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(20))
    sentiment_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Prediction(db.Model):
    """Stored prediction results."""

    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    income = db.Column(db.Float, nullable=False)
    spending_score = db.Column(db.Integer, nullable=False)
    segment = db.Column(db.String(50))
    purchase_probability = db.Column(db.Float)
    churn_risk = db.Column(db.Float)
    clv = db.Column(db.Float)
    recommendations = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class EmailCampaign(db.Model):
    """Email marketing campaign metrics."""

    __tablename__ = "email_campaigns"

    id = db.Column(db.Integer, primary_key=True)
    campaign_name = db.Column(db.String(120), nullable=False)
    emails_sent = db.Column(db.Integer, default=0)
    opens = db.Column(db.Integer, default=0)
    clicks = db.Column(db.Integer, default=0)
    conversions = db.Column(db.Integer, default=0)
    cost = db.Column(db.Float, default=0.0)
    revenue = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CustomerJourney(db.Model):
    """Customer journey funnel events."""

    __tablename__ = "customer_journeys"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(50), nullable=False)
    event_type = db.Column(db.String(30), nullable=False)
    product_id = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Transaction(db.Model):
    """Transactions for fraud detection."""

    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(80))
    is_fraud = db.Column(db.Boolean, default=False)
    fraud_score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class LiveActivity(db.Model):
    """Simulated live customer activity."""

    __tablename__ = "live_activities"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(50))
    activity_type = db.Column(db.String(50))
    value = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
