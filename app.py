"""
AI-Driven Customer Analytics & Business Intelligence Platform
Main Flask application entry point.
"""
import os

import pandas as pd
from sqlalchemy import func, inspect, text
from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from werkzeug.utils import secure_filename

from config import Config
from analytics_routes import analytics_bp
from database import (
    Customer,
    CustomerJourney,
    EmailCampaign,
    Prediction,
    Review,
    Sale,
    Transaction,
    db,
)
from predictor import PredictionService
from recommendation import RecommendationEngine
from report_generator import ReportGenerator
from sentiment import SentimentAnalyzer
from train_model import ModelTrainer

# ---------------------------------------------------------------------------
# Application setup
# ---------------------------------------------------------------------------

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["REPORTS_DIR"], exist_ok=True)

db.init_app(app)
app.register_blueprint(analytics_bp)

predictor = PredictionService()
sentiment_analyzer = SentimentAnalyzer()
report_generator = ReportGenerator()
recommender = RecommendationEngine()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _migrate_schema():
    """Apply schema fixes for legacy databases."""
    inspector = inspect(db.engine)

    if inspector.has_table("predictions"):
        columns = {col["name"] for col in inspector.get_columns("predictions")}
        if "user_id" in columns:
            with db.engine.begin() as conn:
                conn.execute(text("DROP TABLE IF EXISTS predictions"))
                conn.execute(text("DROP TABLE IF EXISTS users"))

    if inspector.has_table("customers"):
        cols = {col["name"] for col in inspector.get_columns("customers")}
        with db.engine.begin() as conn:
            if "predicted_clv" not in cols:
                conn.execute(text("ALTER TABLE customers ADD COLUMN predicted_clv FLOAT DEFAULT 0"))
            if "loyalty_score" not in cols:
                conn.execute(text("ALTER TABLE customers ADD COLUMN loyalty_score FLOAT DEFAULT 0"))


def init_database():
    """Create tables and seed sample data if empty."""
    with app.app_context():
        _migrate_schema()
        db.create_all()
        _seed_data_if_empty()


def _seed_data_if_empty():
    """Load CSV datasets into database on first run."""
    if Customer.query.count() == 0:
        customers_path = os.path.join(app.config["DATASET_DIR"], "customers.csv")
        if os.path.exists(customers_path):
            df = pd.read_csv(customers_path)
            for _, row in df.iterrows():
                db.session.add(
                    Customer(
                        customer_id=str(row["customer_id"]),
                        age=int(row["age"]),
                        income=float(row["income"]),
                        spending_score=int(row["spending_score"]),
                        total_purchases=int(row.get("total_purchases", 0)),
                        churned=bool(row.get("churned", 0)),
                        clv=float(row.get("clv", 0)),
                    )
                )

    if Sale.query.count() == 0:
        sales_path = os.path.join(app.config["DATASET_DIR"], "sales.csv")
        if os.path.exists(sales_path):
            df = pd.read_csv(sales_path)
            for _, row in df.iterrows():
                db.session.add(
                    Sale(
                        month=str(row["month"]),
                        year=int(row["year"]),
                        revenue=float(row["revenue"]),
                        units_sold=int(row.get("units_sold", 0)),
                        product_category=str(row.get("product_category", "")),
                    )
                )

    if Review.query.count() == 0:
        reviews_path = os.path.join(app.config["DATASET_DIR"], "reviews.csv")
        if os.path.exists(reviews_path):
            df = pd.read_csv(reviews_path)
            for _, row in df.iterrows():
                result = sentiment_analyzer.analyze(str(row["review_text"]))
                db.session.add(
                    Review(
                        customer_id=str(row.get("customer_id", "")),
                        review_text=str(row["review_text"]),
                        sentiment=result["sentiment"],
                        sentiment_score=result["score"],
                    )
                )

    if EmailCampaign.query.count() == 0:
        path = os.path.join(app.config["DATASET_DIR"], "campaigns.csv")
        if os.path.exists(path):
            for _, row in pd.read_csv(path).iterrows():
                db.session.add(
                    EmailCampaign(
                        campaign_name=str(row["campaign_name"]),
                        emails_sent=int(row["emails_sent"]),
                        opens=int(row["opens"]),
                        clicks=int(row["clicks"]),
                        conversions=int(row["conversions"]),
                        cost=float(row["cost"]),
                        revenue=float(row["revenue"]),
                    )
                )

    if CustomerJourney.query.count() == 0:
        path = os.path.join(app.config["DATASET_DIR"], "journeys.csv")
        if os.path.exists(path):
            for _, row in pd.read_csv(path).iterrows():
                db.session.add(
                    CustomerJourney(
                        customer_id=str(row["customer_id"]),
                        event_type=str(row["event_type"]),
                        product_id=str(row.get("product_id", "")),
                    )
                )

    if Transaction.query.count() == 0:
        path = os.path.join(app.config["DATASET_DIR"], "transactions.csv")
        if os.path.exists(path):
            for _, row in pd.read_csv(path).iterrows():
                db.session.add(
                    Transaction(
                        customer_id=str(row["customer_id"]),
                        amount=float(row["amount"]),
                        category=str(row.get("category", "")),
                        is_fraud=bool(int(row.get("is_fraud", 0))),
                    )
                )

    db.session.commit()


def get_dashboard_kpis() -> dict:
    """Compute KPI metrics for dashboard cards."""
    total_customers = Customer.query.count()
    total_revenue = db.session.query(func.sum(Sale.revenue)).scalar() or 0
    churned = Customer.query.filter_by(churned=True).count()
    retention_rate = (
        round((1 - churned / total_customers) * 100, 1) if total_customers else 0
    )
    churn_risk_pct = round((churned / total_customers) * 100, 1) if total_customers else 0

    return {
        "total_customers": total_customers,
        "total_revenue": total_revenue,
        "retention_rate": retention_rate,
        "churn_risk": churn_risk_pct,
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    kpis = get_dashboard_kpis()
    return render_template("dashboard.html", kpis=kpis)


@app.route("/api/chart/sales-trend")
def api_sales_trend():
    sales = Sale.query.order_by(Sale.year, Sale.id).all()
    labels = [f"{s.month[:3]} {s.year}" for s in sales]
    data = [s.revenue for s in sales]
    return jsonify({"labels": labels, "data": data})


@app.route("/api/chart/segmentation")
def api_segmentation():
    try:
        data = predictor.get_segment_distribution()
        return jsonify(data)
    except Exception as exc:
        return jsonify({"labels": [], "values": [], "error": str(exc)})


@app.route("/api/chart/forecast")
def api_forecast():
    try:
        forecast = predictor.get_sales_forecast(months_ahead=6)
        return jsonify(forecast)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/api/chart/sentiment")
def api_sentiment():
    """Sentiment distribution for review analysis chart."""
    reviews = Review.query.all()
    counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for review in reviews:
        label = review.sentiment or "Neutral"
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return jsonify({"labels": list(counts.keys()), "values": list(counts.values())})


@app.route("/api/chart/churn")
def api_churn():
    """Churned vs retained customers for bar chart."""
    total = Customer.query.count()
    churned = Customer.query.filter_by(churned=True).count()
    retained = total - churned
    return jsonify({
        "labels": ["Retained", "Churned"],
        "values": [retained, churned],
    })


@app.route("/api/chart/sales-category")
def api_sales_category():
    """Revenue grouped by product category."""
    rows = (
        db.session.query(
            Sale.product_category,
            func.sum(Sale.revenue).label("total"),
        )
        .group_by(Sale.product_category)
        .all()
    )
    return jsonify({
        "labels": [r.product_category or "Other" for r in rows],
        "values": [float(r.total) for r in rows],
    })


@app.route("/api/chart/predictions")
def api_predictions():
    """Recent prediction outcomes: avg purchase probability and churn risk."""
    records = Prediction.query.order_by(Prediction.created_at.desc()).limit(10).all()
    if not records:
        return jsonify({"labels": [], "purchase": [], "churn": []})
    labels = [f"#{r.id}" for r in reversed(records)]
    purchase = [round((r.purchase_probability or 0) * 100, 1) for r in reversed(records)]
    churn = [round((r.churn_risk or 0) * 100, 1) for r in reversed(records)]
    return jsonify({"labels": labels, "purchase": purchase, "churn": churn})


@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    result = None
    if request.method == "POST":
        try:
            age = int(request.form.get("age", 0))
            income = float(request.form.get("income", 0))
            spending_score = int(request.form.get("spending_score", 0))

            if not (18 <= age <= 100):
                flash("Age must be between 18 and 100.", "danger")
            elif income <= 0:
                flash("Income must be greater than 0.", "danger")
            elif not (1 <= spending_score <= 100):
                flash("Spending score must be between 1 and 100.", "danger")
            else:
                result = predictor.predict_all(age, income, spending_score)

                record = Prediction(
                    age=age,
                    income=income,
                    spending_score=spending_score,
                    segment=result["segment"],
                    purchase_probability=result["purchase_probability"],
                    churn_risk=result["churn_risk"],
                    clv=result["clv"],
                    recommendations=recommender.format_recommendations(result["segment"]),
                )
                db.session.add(record)
                db.session.commit()
                flash("Prediction completed successfully.", "success")
        except FileNotFoundError:
            flash("ML models not found. Please upload data and train models first.", "warning")
        except Exception as exc:
            flash(f"Prediction error: {exc}", "danger")

    return render_template("prediction.html", result=result)


@app.route("/reviews", methods=["GET", "POST"])
def reviews():
    analysis_result = None
    if request.method == "POST":
        text = request.form.get("review_text", "").strip()
        if not text:
            flash("Please enter review text.", "danger")
        else:
            analysis_result = sentiment_analyzer.analyze(text)
            db.session.add(
                Review(
                    customer_id="guest",
                    review_text=text,
                    sentiment=analysis_result["sentiment"],
                    sentiment_score=analysis_result["score"],
                )
            )
            db.session.commit()

    recent_reviews = Review.query.order_by(Review.created_at.desc()).limit(10).all()
    return render_template(
        "reviews.html",
        analysis_result=analysis_result,
        recent_reviews=recent_reviews,
    )


@app.route("/reports")
def reports():
    predictions = (
        Prediction.query.order_by(Prediction.created_at.desc()).limit(20).all()
    )
    return render_template("reports.html", predictions=predictions)


@app.route("/reports/generate/<int:prediction_id>")
def generate_report(prediction_id):
    record = Prediction.query.get_or_404(prediction_id)

    data = {
        "age": record.age,
        "income": record.income,
        "spending_score": record.spending_score,
        "segment": record.segment,
        "purchase_probability": record.purchase_probability,
        "churn_risk": record.churn_risk,
        "clv": record.clv,
        "recommendations": recommender.get_recommendations(record.segment or ""),
    }
    filepath = report_generator.generate_customer_report(data)
    return send_file(filepath, as_attachment=True)


ALLOWED_EXTENSIONS = {"csv"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        dataset_type = request.form.get("dataset_type", "customers")
        file = request.files.get("file")

        if not file or file.filename == "":
            flash("No file selected.", "danger")
            return redirect(url_for("upload"))

        if not allowed_file(file.filename):
            flash("Only CSV files are allowed.", "danger")
            return redirect(url_for("upload"))

        filename = secure_filename(file.filename)
        target_name = f"{dataset_type}.csv"
        save_path = os.path.join(app.config["DATASET_DIR"], target_name)
        upload_copy = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)
        file.seek(0)
        file.save(upload_copy)

        try:
            df = pd.read_csv(save_path)
            if dataset_type == "customers":
                _import_customers_csv(df)
            elif dataset_type == "sales":
                _import_sales_csv(df)
            elif dataset_type == "reviews":
                _import_reviews_csv(df)

            ModelTrainer().train_all()
            predictor._models_loaded = False
            flash(f"{dataset_type.title()} dataset uploaded and models retrained.", "success")
        except Exception as exc:
            flash(f"Upload processing error: {exc}", "danger")

        return redirect(url_for("upload"))

    return render_template("upload.html")


def _import_customers_csv(df: pd.DataFrame):
    Customer.query.delete()
    for _, row in df.iterrows():
        db.session.add(
            Customer(
                customer_id=str(row.get("customer_id", f"C{row.name}")),
                age=int(row["age"]),
                income=float(row["income"]),
                spending_score=int(row["spending_score"]),
                total_purchases=int(row.get("total_purchases", 0)),
                churned=bool(row.get("churned", 0)),
                clv=float(row.get("clv", 0)),
            )
        )
    db.session.commit()


def _import_sales_csv(df: pd.DataFrame):
    Sale.query.delete()
    for _, row in df.iterrows():
        db.session.add(
            Sale(
                month=str(row["month"]),
                year=int(row["year"]),
                revenue=float(row["revenue"]),
                units_sold=int(row.get("units_sold", 0)),
                product_category=str(row.get("product_category", "")),
            )
        )
    db.session.commit()


def _import_reviews_csv(df: pd.DataFrame):
    for _, row in df.iterrows():
        result = sentiment_analyzer.analyze(str(row["review_text"]))
        db.session.add(
            Review(
                customer_id=str(row.get("customer_id", "")),
                review_text=str(row["review_text"]),
                sentiment=result["sentiment"],
                sentiment_score=result["score"],
            )
        )
    db.session.commit()


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(error):
    return render_template("base.html"), 404


@app.errorhandler(500)
def server_error(error):
    flash("An internal error occurred.", "danger")
    return redirect(url_for("dashboard"))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    init_database()
    models_path = os.path.join(app.config["MODELS_DIR"], "segmentation.pkl")
    if not os.path.exists(models_path):
        print("Training ML models...")
        ModelTrainer().train_all()
    app.run(debug=True, host="0.0.0.0", port=5000)
