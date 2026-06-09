# AI-Driven Customer Analytics & Business Intelligence Platform

A full-stack Flask application for customer segmentation, purchase/churn prediction, CLV estimation, sales forecasting, sentiment analysis, and PDF reporting.

> **Problem Statement:** See [PROBLEM_STATEMENT.md](PROBLEM_STATEMENT.md) for the project problem definition, objectives, and expected outcomes.
>
> **All Graphs:** See [GRAPHS_DOCUMENTATION.md](GRAPHS_DOCUMENTATION.md) for descriptions of every chart and KPI (purpose, data source, ML model, business insight).

## Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy, Werkzeug
- **Database:** MySQL (production) / SQLite (default for local dev)
- **ML:** Scikit-learn, Pandas, NumPy, Joblib
- **NLP:** TextBlob
- **Reports:** ReportLab
- **Frontend:** Bootstrap 5, Chart.js, JavaScript

## Features

- K-Means customer segmentation
- Random Forest purchase & churn prediction
- Linear Regression CLV prediction
- Sales revenue forecasting
- Product recommendations by segment
- Sentiment analysis on reviews
- Interactive dashboard with Chart.js
- PDF report generation
- CSV dataset upload with auto model retraining

## Project Structure

```
AI-Customer-Analytics/
├── app.py                  # Main Flask application
├── config.py               # Configuration
├── database.py             # SQLAlchemy models
├── train_model.py          # ML model training
├── predictor.py            # Prediction service
├── recommendation.py       # Product recommendations
├── sentiment.py            # Sentiment analysis
├── report_generator.py     # PDF reports
├── requirements.txt
├── dataset/                # CSV datasets
├── models/                 # Trained .pkl models
├── templates/              # HTML templates
├── static/                 # CSS, JS, images
└── reports/                # Generated PDFs
```

## Setup Instructions

### 1. Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
python -m textblob.download_corpora
```

### 3. Database configuration

**SQLite (default):** No setup required.

**MySQL:** Create database and set environment variable:

```sql
CREATE DATABASE ai_customer_analytics;
```

```bash
# Windows PowerShell
$env:DATABASE_URL = "mysql+pymysql://root:password@localhost/ai_customer_analytics"

# Linux/macOS
export DATABASE_URL="mysql+pymysql://root:password@localhost/ai_customer_analytics"
```

### 4. Train ML models

```bash
python train_model.py
```

### 5. Run the application

```bash
python app.py
```

Open **http://localhost:5000** in your browser. The dashboard loads directly with no login required.

## API Endpoints

| Route | Description |
|-------|-------------|
| `/` | Redirect to dashboard |
| `/dashboard` | Analytics dashboard |
| `/prediction` | Customer prediction form |
| `/reviews` | Sentiment analysis |
| `/reports` | PDF report downloads |
| `/upload` | CSV dataset upload |
| `/api/chart/sales-trend` | Sales trend JSON |
| `/api/chart/segmentation` | Segmentation pie chart JSON |
| `/api/chart/forecast` | Revenue forecast JSON |
| `/api/chart/sentiment` | Sentiment distribution JSON |
| `/api/chart/churn` | Churn vs retained JSON |
| `/api/chart/sales-category` | Revenue by category JSON |
| `/api/chart/predictions` | Recent prediction trends JSON |

## Database Tables

- `customers` — Customer records
- `sales` — Monthly sales data
- `reviews` — Customer reviews with sentiment
- `predictions` — Stored prediction results

## License

Educational / portfolio project.
