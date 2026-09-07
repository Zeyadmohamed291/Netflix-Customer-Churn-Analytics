# 🎬 Netflix Customer Churn & Engagement Dataset

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)
[![Kaggle Ready](https://img.shields.io/badge/Kaggle-Dataset_Card-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com)
[![Records: 5,000](https://img.shields.io/badge/Records-5%2C000-E50914)](file:///netflix_customer_churn.csv)
[![Features: 14](https://img.shields.io/badge/Features-14-black)](file:///netflix_customer_churn.csv)

A comprehensive, curated dataset analyzing customer churn dynamics, behavioral engagement, subscription economics, and demographics for **5,000 Netflix subscribers** across 6 global continents.

---

## 📌 Context & Business Problem
Customer churn (subscriber attrition) is one of the most critical challenges facing global streaming platforms. Acquiring a new customer often costs 5 to 7 times more than retaining an existing one. 

This dataset tracks user engagement, hardware utilization, billing mechanisms, and account inactivity to help data scientists and analysts uncover:
1. **Early Attrition Indicators:** What behavioral signals (e.g., login inactivity, declining watch hours) predict churn before it happens?
2. **Subscription Tier Viability:** How do churn rates differ between Basic ($8.99), Standard ($13.99), and Premium ($17.99) plans?
3. **Regional & Demographic Dynamics:** Which geographic markets and age cohorts represent the highest retention or attrition risk?
4. **Payment Gateway Friction:** Does payment method (e.g., Crypto, Gift Card vs Credit/Debit) impact customer lifetime value?

---

## 🗂️ Data Dictionary

The dataset consists of **5,000 unique subscriber records** with **14 attributes** and zero missing values:

| Column Name | Data Type | Range / Distinct Values | Description |
|---|---|---|---|
| `customer_id` | `string` | UUID format (e.g. `a9b75100-...`) | Unique anonymous subscriber identifier. |
| `age` | `integer` | `18` to `70` years | Customer age in completed years. |
| `gender` | `string` | `Female`, `Male`, `Other` | Customer demographic self-identification. |
| `subscription_type` | `string` | `Basic`, `Standard`, `Premium` | Current Netflix subscription tier. |
| `watch_hours` | `float` | `0.10` to `110.40` hrs | Total cumulative monthly streaming hours. |
| `last_login_days` | `integer` | `0` to `60` days | Number of days elapsed since the subscriber last logged in. |
| `region` | `string` | `Africa`, `Asia`, `Europe`, `North America`, `Oceania`, `South America` | Primary geographic operational market. |
| `device` | `string` | `Desktop`, `Laptop`, `Mobile`, `TV`, `Tablet` | Primary viewing hardware platform. |
| `monthly_fee` | `float` | `8.99`, `13.99`, `17.99` (USD) | Regular monthly recurring fee billed to account. |
| `churned` | `integer` | `0` (Active), `1` (Churned) | **Target variable**: whether subscriber cancelled service. |
| `payment_method` | `string` | `Credit Card`, `Crypto`, `Debit Card`, `Gift Card`, `PayPal` | Payment method registered on the billing profile. |
| `number_of_profiles` | `integer` | `1` to `5` | Active viewer sub-profiles on account. |
| `avg_watch_time_per_day` | `float` | `0.01` to `4.97` hrs | Calculated daily streaming engagement average. |
| `favorite_genre` | `string` | `Action`, `Comedy`, `Drama`, `Horror`, `Romance`, `Sci-Fi`, `Thriller` | Most frequently streamed content genre. |

---

## 📊 Summary Statistics & Benchmark Baselines

- **Total Subscribers:** 5,000
- **Active Retained Subscribers (`churned = 0`):** 2,485 (49.70%)
- **Churned Subscribers (`churned = 1`):** 2,515 (50.30%)
- **Average Customer Age:** 43.85 years
- **Average Monthly Watch Hours:** 11.65 hours
- **Average Inactivity Window:** 24.81 days
- **Top Subscription Tier by Volume:** Premium (1,693 subscribers)
- **Top Region by Volume:** South America (873 subscribers)
- **Top Device Platform:** Tablet (1,048 subscribers)

---

## 🔍 Key Exploratory Insights

1. **The 30-Day Inactivity Tipping Point:**
   - Subscribers inactive for `0-10 days` experience a low **18.3%** churn rate.
   - Once inactivity crosses `30 days`, churn jumps dramatically to over **72.5%**, peaking at **78.1%** for 40-50 days.
2. **Plan Tier Attrition:**
   - `Basic` tier customers experience the highest churn rate (~**61.8%**).
   - `Premium` tier customers maintain significantly stronger retention and engagement.
3. **Billing Stability:**
   - Subscribers paying via `Crypto` and `Gift Card` exhibit the highest attrition risk (~**59.7%**), whereas direct `Credit/Debit Card` users demonstrate higher loyalty.

---

## 🚀 Starter Python Code

```python
import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("netflix_customer_churn.csv")

# Quick verification
print("Dataset Shape:", df.shape)
print("Missing values:\n", df.isnull().sum())

# Overall churn rate
churn_rate = df["churned"].mean() * 100
print(f"Overall Churn Rate: {churn_rate:.2f}%")

# Churn rate by subscription type
plan_churn = df.groupby("subscription_type")["churned"].mean() * 100
print("\nChurn by Plan Tier (%):\n", plan_churn.sort_values(ascending=False))

# Churn rate by inactivity brackets
bins = [0, 10, 20, 30, 40, 50, 60]
labels = ["0-10d", "11-20d", "21-30d", "31-40d", "41-50d", "51-60d"]
df["inactivity_group"] = pd.cut(df["last_login_days"], bins=bins, labels=labels)
inactivity_churn = df.groupby("inactivity_group", observed=False)["churned"].mean() * 100
print("\nChurn by Inactivity Cohort (%):\n", inactivity_churn)
```

---

## 💡 Potential Tasks & Challenges for Kaggle Users

1. **Supervised Classification:**
   - Build and compare models (Logistic Regression, Random Forest, XGBoost, CatBoost, LightGBM) to classify subscriber churn (`ROC-AUC`, `F1-Score`, `Precision-Recall`).
2. **Feature Importance & Interpretability:**
   - Use SHAP (SHapley Additive exPlanations) to identify the driving factors behind churn decisions.
3. **Customer Segmentation & Clustering:**
   - Perform unsupervised clustering (K-Means, DBSCAN) using watch hours, daily streaming duration, and profile counts to identify distinct subscriber personas (e.g. "Binge Watchers", "Casual Viewers", "Dormant Accounts").
4. **Interactive Dashboarding:**
   - Explore and run the included Streamlit analytics app ([`streamlit_app.py`](file:///streamlit_app.py)) featuring full Power BI-style dark UX.

---

## 📜 License
This dataset is published under the **Creative Commons Zero 1.0 (CC0 1.0) Public Domain Dedication**. You are free to copy, modify, distribute, and perform work with the dataset for academic, personal, or commercial purposes without seeking permission.
