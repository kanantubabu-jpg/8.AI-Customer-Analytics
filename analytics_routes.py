"""
Advanced analytics routes — one dedicated graph page per module.
"""
from flask import Blueprint, jsonify, render_template, request, session

from analytics_service import AnalyticsService

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")
service = AnalyticsService()

# Each module: slug, title, description, API endpoint, chart type, roles allowed
ANALYTICS_MODULES = [
    {
        "slug": "predicted-clv",
        "title": "Predicted CLV",
        "description": "AI-predicted Customer Lifetime Value for top customers using Linear Regression.",
        "api": "/analytics/api/predicted-clv",
        "chart_type": "bar",
        "roles": ["data_analyst", "marketing_manager", "viewer"],
    },
    {
        "slug": "email-campaigns",
        "title": "Email Campaign Tracking",
        "description": "Track emails sent, opens, clicks, and conversions per campaign.",
        "api": "/analytics/api/email-campaigns",
        "chart_type": "grouped_bar",
        "roles": ["data_analyst", "marketing_manager"],
    },
    {
        "slug": "campaign-roi",
        "title": "Campaign ROI Prediction",
        "description": "Actual vs ML-predicted return on investment for marketing campaigns.",
        "api": "/analytics/api/campaign-roi",
        "chart_type": "line",
        "roles": ["data_analyst", "marketing_manager"],
    },
    {
        "slug": "best-targets",
        "title": "Best Customer Targets",
        "description": "Highest-value customers ranked by conversion probability, loyalty, and CLV.",
        "api": "/analytics/api/best-targets",
        "chart_type": "horizontal_bar",
        "roles": ["data_analyst", "marketing_manager"],
    },
    {
        "slug": "conversion-probability",
        "title": "Conversion Probability by Segment",
        "description": "Average purchase conversion probability per AI customer segment.",
        "api": "/analytics/api/conversion-probability",
        "chart_type": "bar",
        "roles": ["data_analyst", "marketing_manager", "viewer"],
    },
    {
        "slug": "loyalty-score",
        "title": "Loyalty Score",
        "description": "Loyalty = Purchase Frequency + Average Spending + Review Sentiment.",
        "api": "/analytics/api/loyalty-score",
        "chart_type": "stacked_bar",
        "roles": ["data_analyst", "marketing_manager", "viewer"],
    },
    {
        "slug": "purchase-history",
        "title": "Purchase History",
        "description": "Total purchase count per customer from historical records.",
        "api": "/analytics/api/purchase-history",
        "chart_type": "bar",
        "roles": ["data_analyst", "viewer"],
    },
    {
        "slug": "fraud-detection",
        "title": "Fraud Detection",
        "description": "ML identifies fake transactions, suspicious spending, and abnormal behavior.",
        "api": "/analytics/api/fraud-detection",
        "chart_type": "doughnut",
        "roles": ["data_analyst"],
    },
    {
        "slug": "customer-journey",
        "title": "Customer Journey Analytics",
        "description": "Funnel: Visit → View Product → Add To Cart → Purchase.",
        "api": "/analytics/api/customer-journey",
        "chart_type": "funnel_bar",
        "roles": ["data_analyst", "marketing_manager", "viewer"],
    },
    {
        "slug": "live-sales",
        "title": "Live Sales",
        "description": "Real-time sales stream with auto-refresh every 10 seconds.",
        "api": "/analytics/api/live-sales",
        "chart_type": "line",
        "live": True,
        "roles": ["data_analyst", "marketing_manager"],
    },
    {
        "slug": "live-activity",
        "title": "Live Customer Activity",
        "description": "Live browse, cart, purchase, and review activity counts.",
        "api": "/analytics/api/live-activity",
        "chart_type": "bar",
        "live": True,
        "roles": ["data_analyst", "marketing_manager"],
    },
    {
        "slug": "collaborative-filtering",
        "title": "Collaborative Filtering",
        "description": "Product recommendations from user-item interaction patterns.",
        "api": "/analytics/api/collaborative-filtering",
        "chart_type": "bar",
        "roles": ["data_analyst", "marketing_manager"],
    },
    {
        "slug": "matrix-factorization",
        "title": "Matrix Factorization (NMF)",
        "description": "Non-negative Matrix Factorization latent factor strengths.",
        "api": "/analytics/api/matrix-factorization",
        "chart_type": "bar",
        "roles": ["data_analyst"],
    },
    {
        "slug": "hybrid-recommender",
        "title": "Hybrid Recommender System",
        "description": "Combines Collaborative Filtering + Content-Based recommendations.",
        "api": "/analytics/api/hybrid-recommender",
        "chart_type": "multi_line",
        "roles": ["data_analyst", "marketing_manager"],
    },
]

ROLE_LABELS = {
    "data_analyst": "Data Analyst",
    "marketing_manager": "Marketing Manager",
    "viewer": "Viewer",
}


def _current_role():
    return session.get("user_role", "data_analyst")


def _modules_for_role(role: str) -> list:
    return [m for m in ANALYTICS_MODULES if role in m["roles"]]


@analytics_bp.route("/")
def analytics_hub():
    role = _current_role()
    return render_template(
        "analytics/hub.html",
        modules=_modules_for_role(role),
        role=role,
        role_label=ROLE_LABELS.get(role, role),
    )


@analytics_bp.route("/set-role", methods=["POST"])
def set_role():
    role = request.form.get("role", "data_analyst")
    if role in ROLE_LABELS:
        session["user_role"] = role
    return jsonify({"role": role, "label": ROLE_LABELS[role]})


@analytics_bp.route("/<slug>")
def analytics_page(slug):
    module = next((m for m in ANALYTICS_MODULES if m["slug"] == slug), None)
    if not module:
        return "Not found", 404
    if _current_role() not in module["roles"]:
        return render_template("analytics/denied.html", module=module), 403
    return render_template("analytics/chart_page.html", module=module)


# API endpoints
@analytics_bp.route("/api/predicted-clv")
def api_predicted_clv():
    return jsonify(service.predicted_clv_chart())


@analytics_bp.route("/api/email-campaigns")
def api_email_campaigns():
    return jsonify(service.email_campaign_chart())


@analytics_bp.route("/api/campaign-roi")
def api_campaign_roi():
    return jsonify(service.campaign_roi_chart())


@analytics_bp.route("/api/best-targets")
def api_best_targets():
    return jsonify(service.best_targets_chart())


@analytics_bp.route("/api/conversion-probability")
def api_conversion():
    return jsonify(service.conversion_by_segment_chart())


@analytics_bp.route("/api/loyalty-score")
def api_loyalty():
    return jsonify(service.loyalty_chart())


@analytics_bp.route("/api/purchase-history")
def api_purchase_history():
    return jsonify(service.purchase_history_chart())


@analytics_bp.route("/api/fraud-detection")
def api_fraud():
    return jsonify(service.fraud_chart())


@analytics_bp.route("/api/customer-journey")
def api_journey():
    return jsonify(service.journey_funnel_chart())


@analytics_bp.route("/api/live-sales")
def api_live_sales():
    return jsonify(service.live_sales_chart())


@analytics_bp.route("/api/live-activity")
def api_live_activity():
    return jsonify(service.live_activity_chart())


@analytics_bp.route("/api/collaborative-filtering")
def api_cf():
    return jsonify(service.collaborative_filtering_chart())


@analytics_bp.route("/api/matrix-factorization")
def api_mf():
    return jsonify(service.matrix_factorization_chart())


@analytics_bp.route("/api/hybrid-recommender")
def api_hybrid():
    return jsonify(service.hybrid_recommender_chart())
