# Problem Statement — AI-Driven Customer Analytics Platform

## 1. Background

Modern businesses collect large volumes of customer data — demographics, purchase history, spending behaviour, sales records, and product reviews. However, most organisations rely on spreadsheets or basic reporting tools that only summarise what has already happened. They cannot answer forward-looking questions such as *who will churn*, *who is likely to buy next*, or *which products suit each customer group*.

## 2. Problem Definition

Organisations face the following challenges when managing customer relationships without intelligent analytics:

| Challenge | Impact |
|-----------|--------|
| Fragmented customer data across sales, reviews, and profiles | No single view of customer health |
| Manual segmentation of customers by age, income, and spending | Slow, inconsistent, and not scalable |
| No predictive insight into purchase intent or churn risk | Reactive instead of proactive retention |
| Static dashboards with historical numbers only | Missed opportunities for forecasting and planning |
| Unstructured review text left unanalysed | Customer sentiment and pain points stay hidden |
| Generic product offers for all customers | Lower conversion and weaker loyalty |

Traditional Business Intelligence (BI) tools report past revenue and customer counts but lack machine learning models to classify segments, estimate Customer Lifetime Value (CLV), forecast future sales, or recommend products per segment.

## 3. Proposed Solution (This Platform)

The **AI-Driven Customer Analytics & Business Intelligence Platform** addresses these gaps through an integrated web application that combines:

- **K-Means clustering** — automatically groups customers into segments (e.g. Budget Conscious, Premium Loyalists) from age, income, and spending score.
- **Random Forest classifiers** — predict purchase probability and churn risk for individual customers.
- **Linear regression** — estimate CLV and forecast monthly revenue trends.
- **Sentiment analysis (TextBlob)** — classify review text as Positive, Negative, or Neutral with polarity scores.
- **Segment-based product recommendations** — suggest relevant products after each prediction.
- **Interactive dashboard (Chart.js)** — live KPI cards (total customers, revenue, retention rate, churn risk) plus sales trend, segmentation pie chart, and revenue forecast charts.
- **PDF report generation** — downloadable reports with prediction results and recommendations.
- **CSV dataset upload** — retrain all models when new customer, sales, or review data is uploaded.

Data is stored in a relational database (MySQL / SQLite) with dedicated tables for customers, sales, reviews, and predictions, ensuring persistence and traceability of analytics outputs.

## 4. Objectives

1. Provide a unified dashboard for real-time business KPIs and visual analytics.
2. Enable data-driven customer segmentation without manual rule writing.
3. Support predictive decisions on purchases, churn, and lifetime value.
4. Turn unstructured reviews into actionable sentiment insights.
5. Personalise product recommendations based on predicted customer segment.
6. Forecast future sales revenue to support planning and inventory decisions.
7. Allow non-technical users to refresh models by uploading updated CSV datasets.

## 5. Expected Outcomes

By deploying this platform, businesses can:

- Reduce customer churn through early risk identification.
- Increase revenue via targeted recommendations and better segment understanding.
- Improve marketing ROI by focusing on high-value and at-risk segments.
- Monitor brand perception through automated review sentiment tracking.
- Replace static reports with dynamic, AI-powered business intelligence.

## 6. Scope

**In scope:** Customer analytics dashboard, ML-based predictions, sentiment analysis, sales forecasting, PDF reports, and dataset upload with automatic model retraining.

**Out of scope:** Real-time payment processing, CRM integration with third-party APIs, and multi-tenant user authentication (current version is open access for demonstration and academic use).

## 7. Conclusion

There is a clear need for an AI-driven customer analytics platform that moves beyond historical reporting. This project delivers that capability by unifying statistical analysis, machine learning, natural language processing, and modern data visualisation in a single Flask-based application — helping organisations understand customer behaviour, predict future actions, and personalise engagement to drive sustainable growth.
