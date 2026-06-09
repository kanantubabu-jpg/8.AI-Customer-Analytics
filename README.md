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

<img width="1081" height="623" alt="Screenshot 2026-06-08 152120" src="https://github.com/user-attachments/assets/9bfd8e46-d7eb-426b-b523-12279b4b8643" />

<img width="1918" height="1012" alt="Screenshot 2026-06-08 152147" src="https://github.com/user-attachments/assets/f6864ab7-504c-4d87-b14e-08972255aa13" />

<img width="1918" height="931" alt="Screenshot 2026-06-08 152217" src="https://github.com/user-attachments/assets/83a74b7d-c6a4-42e7-891d-c98bbbc8e072" />


<img width="1918" height="1017" alt="Screenshot 2026-06-08 152240" src="https://github.com/user-attachments/assets/d071d3a2-25a3-42fe-8145-c540120066ed" />

<img width="1918" height="993" alt="Screenshot 2026-06-08 152308" src="https://github.com/user-attachments/assets/e6b32219-cfe3-4552-b1bc-a46f36c50684" />

<img width="1918" height="1018" alt="Screenshot 2026-06-08 152328" src="https://github.com/user-attachments/assets/e98c525f-ba0b-400c-9b1c-33613b5c83a7" />

<img width="1918" height="1001" alt="Screenshot 2026-06-08 152343" src="https://github.com/user-attachments/assets/675cb7de-62e1-48c6-be94-c26ca6b2bf79" />

<img width="1918" height="963" alt="Screenshot 2026-06-08 152406" src="https://github.com/user-attachments/assets/649f3c55-a163-48c5-a485-e6173450dbb6" />



<img width="1918" height="948" alt="Screenshot 2026-06-08 152440" src="https://github.com/user-attachments/assets/48076083-5297-43cb-aa98-369430511bfe" />

<img width="1918" height="1011" alt="Screenshot 2026-06-08 152457" src="https://github.com/user-attachments/assets/a49f63d4-215c-41c7-8dbf-8276bf75f475" />



<img width="1918" height="1002" alt="Screenshot 2026-06-08 152522" src="https://github.com/user-
  attachments/assets/6c18fc6d-2e66-491b-8b8d-6abef5b8ef9b" />


<img width="1918" height="975" alt="Screenshot 2026-06-08 152510" src="https://github.com/user-attachments/assets/3a3826fc-f864-4442-96f1-4b685565ee34" />

# AI-Driven Customer Analytics & Business Intelligence Platform

Developed a full-stack AI-powered Customer Analytics and Business Intelligence Platform using Flask, Machine Learning, NLP, and Business Intelligence techniques to help organizations analyze customer behavior, predict future trends, and make data-driven decisions.

The platform performs customer segmentation using K-Means clustering, predicts customer churn and purchase likelihood using Random Forest models, estimates Customer Lifetime Value (CLV) through Linear Regression, and forecasts future sales revenue using predictive analytics. It also incorporates sentiment analysis on customer reviews using Natural Language Processing (TextBlob) to measure customer satisfaction and brand perception.

The system features an interactive analytics dashboard built with Bootstrap and Chart.js, providing real-time visualizations of customer segments, sales trends, churn analysis, sentiment distribution, and revenue forecasts. Users can upload new datasets in CSV format, automatically retrain machine learning models, generate business insights, and download professional PDF reports.

Key Features:

* Customer Segmentation using K-Means Clustering
* Purchase & Churn Prediction using Random Forest
* Customer Lifetime Value (CLV) Estimation
* Sales Revenue Forecasting
* Product Recommendation Engine
* Sentiment Analysis on Customer Reviews
* Interactive Business Intelligence Dashboard
* Automated PDF Report Generation
* CSV Dataset Upload and Model Retraining
* MySQL/SQLite Database Integration

Technologies Used:
Flask, Python, Scikit-learn, Pandas, NumPy, TextBlob, SQLAlchemy, MySQL, SQLite, Bootstrap 5, Chart.js, JavaScript, ReportLab, Joblib.

Outcome:
The platform transforms raw customer and sales data into actionable business intelligence, enabling organizations to improve customer retention, increase revenue, optimize marketing strategies, and support data-driven decision-making.
