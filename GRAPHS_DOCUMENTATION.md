# Graphs & Visualizations Documentation

This document describes **all charts and KPIs** in the AI Customer Analytics platform — what problem each solves, data source, chart type, and business insight. Use this for project reports, viva, and documentation (not displayed on the website).

---

## KPI Cards (Summary Metrics)

| KPI | Problem Addressed | Data Source | Insight |
|-----|-------------------|-------------|---------|
| **Total Customers** | No quick view of customer base size | `customers` table | Shows how many customer records are in the system |
| **Revenue** | Revenue scattered across months, hard to see total | `sales` table (sum of revenue) | Total business revenue from all sales records |
| **Retention Rate** | Cannot measure loyalty without churn tracking | Customers where `churned = false` | Percentage of customers still active |
| **Churn Risk** | Late discovery of customer loss | Customers where `churned = true` | Percentage of customers who have churned |

---

## Graph 1 — Sales Trend (Line Chart)

| Item | Detail |
|------|--------|
| **Chart Type** | Line Chart |
| **API** | `GET /api/chart/sales-trend` |
| **Data Source** | `sales` table — month, year, revenue |
| **Technology** | Chart.js |

**Problem:** Businesses cannot easily see whether revenue is growing or declining over time when data sits in raw CSV or database rows.

**Solution:** Plots monthly revenue as a continuous trend line so managers can spot seasonality, growth, and dips at a glance.

**Business Insight:** Identifies peak sales months and downward trends for inventory and marketing planning.

---

## Graph 2 — Customer Segmentation (Pie Chart)

| Item | Detail |
|------|--------|
| **Chart Type** | Pie Chart |
| **API** | `GET /api/chart/segmentation` |
| **Data Source** | `customers.csv` + K-Means model (`segmentation.pkl`) |
| **ML Model** | K-Means Clustering (4 segments) |
| **Segments** | Budget Conscious, Standard Shoppers, Premium Loyalists, High-Value Champions |

**Problem:** Manual customer grouping by age or income alone is inconsistent and does not reflect combined behaviour.

**Solution:** AI clusters every customer using age, income, and spending score, then shows segment share as a pie chart.

**Business Insight:** Reveals which customer groups dominate the base and where to focus campaigns.

---

## Graph 3 — Revenue Forecast (Bar Chart)

| Item | Detail |
|------|--------|
| **Chart Type** | Grouped Bar Chart |
| **API** | `GET /api/chart/forecast` |
| **Data Source** | `sales` table + Linear Regression (`sales_forecast.pkl`) |
| **ML Model** | Linear Regression on monthly period index |

**Problem:** Historical reports do not answer “what will revenue look like next quarter?”

**Solution:** Compares actual past revenue (blue bars) with model-predicted future revenue (orange bars) for the next 6 months.

**Business Insight:** Supports budget forecasting, staffing, and stock decisions.

---

## Graph 4 — Churn Analysis (Doughnut Chart)

| Item | Detail |
|------|--------|
| **Chart Type** | Doughnut Chart |
| **API** | `GET /api/chart/churn` |
| **Data Source** | `customers` table — `churned` field |

**Problem:** Churn rate is often buried in spreadsheets without a clear visual split.

**Solution:** Shows retained vs churned customers as two segments in one chart.

**Business Insight:** Quick health check of customer loyalty; high churn slice triggers retention actions.

---

## Graph 5 — Sentiment Distribution (Pie Chart)

| Item | Detail |
|------|--------|
| **Chart Type** | Pie Chart |
| **API** | `GET /api/chart/sentiment` |
| **Data Source** | `reviews` table — sentiment labels |
| **NLP** | TextBlob polarity → Positive / Negative / Neutral |

**Problem:** Customer feedback in text form is unreadable at scale; brand perception stays hidden.

**Solution:** Aggregates all analysed reviews into sentiment counts and displays proportion per category.

**Business Insight:** Detects overall satisfaction; rising negative share signals product or service issues.

---

## Graph 6 — Sales by Category (Bar Chart)

| Item | Detail |
|------|--------|
| **Chart Type** | Bar Chart |
| **API** | `GET /api/chart/sales-category` |
| **Data Source** | `sales` table grouped by `product_category` |

**Problem:** Total revenue alone does not show which product lines drive income.

**Solution:** Bars compare total revenue per category (Electronics, Clothing, Home, Sports, etc.).

**Business Insight:** Highlights best-performing categories for promotions and inventory focus.

---

## Graph 7 — Recent Predictions (Line Chart)

| Item | Detail |
|------|--------|
| **Chart Type** | Multi-line Chart |
| **API** | `GET /api/chart/predictions` |
| **Data Source** | `predictions` table (last 10 records) |
| **ML Models** | Random Forest (purchase & churn) |

**Problem:** Individual prediction results are not compared over time after users run the prediction form.

**Solution:** Plots purchase probability % and churn risk % for each recent prediction side by side.

**Business Insight:** Tracks how model outputs vary across different customer profiles entered on the prediction page.

---

## Summary Table — All Graphs

| # | Graph Name | Type | Module |
|---|------------|------|--------|
| 1 | Sales Trend | Line | Sales Analytics |
| 2 | Customer Segmentation | Pie | AI Segmentation |
| 3 | Revenue Forecast | Bar | Sales Forecasting |
| 4 | Churn Analysis | Doughnut | Customer Analytics |
| 5 | Sentiment Distribution | Pie | Sentiment Analysis |
| 6 | Sales by Category | Bar | Sales Analytics |
| 7 | Recent Predictions | Line | Prediction Module |

---

## How Data Flows to Charts

```
CSV Datasets → Database Tables → Flask API → Chart.js → Dashboard
                    ↓
              ML Models (train_model.py)
              - segmentation.pkl
              - sales_forecast.pkl
              - purchase.pkl / churn.pkl
```

All charts load dynamically via JavaScript `fetch()` calls — no page reload required. Upload new CSV data on the **Upload** page to refresh underlying data and retrain models.
