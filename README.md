# 🎬 Netflix Customer Churn Analytics Dashboard

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.62-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-7.0-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.2-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.10-11557C?style=for-the-badge&logo=python&logoColor=white)
[![Kaggle Dataset](https://img.shields.io/badge/Kaggle-Gold_10.0-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/datasets/zeyadmohamed26/netflix-customer-churn-and-engagement-analytics)
[![Live Demo](https://img.shields.io/badge/Live_Dashboard-Streamlit_Cloud-E50914?style=for-the-badge&logo=netflix&logoColor=white)](https://netflix-customer-churn-analytics-nm53kpy7xfqu4usyxlufym.streamlit.app)

**A professional, dark-themed interactive dashboard and analytical suite for exploring Netflix customer churn data — featuring 30 business questions with full code, results, Plotly visualizations, and a publication-ready Kaggle dataset card.**

👉 **[Launch Live Dashboard](https://netflix-customer-churn-analytics-nm53kpy7xfqu4usyxlufym.streamlit.app)** 👈

</div>

---

## 📸 Dashboard Preview

| Feature | Description |
|---|---|
| 🏠 **Power BI Style Executive Overview** | Headline KPIs (Total/Active/Churned), Choropleth world map, Device breakdown, Genre distribution, Retention donut, Inactivity churn curve |
| 👥 **Customer Analytics** | Audience segmentation by region, hardware device, subscription tiers & daily watch duration |
| 📉 **Churn Intelligence** | Subscriber attrition velocity across subscription tiers, geographic markets, payment gateways, and usage metrics |
| ❓ **30 Business Questions** | Each with business objective, strategic value, executable Python code, result table & Matplotlib chart |
| 🗃️ **Data Explorer** | Filtered records viewer, descriptive statistics, data quality indicators & segment CSV export |

---

## 🚀 Quick Start (Setup on Any Computer)

### Prerequisites

- **Python 3.10+** installed — [Download Python](https://www.python.org/downloads/)

### Step 1: Download the Code

1. Open the repository on GitHub: [Netflix-Customer-Churn-Analytics](https://github.com/Zeyadmohamed291/Netflix-Customer-Churn-Analytics)
2. Click the green **Code** button and select **Download ZIP**.
3. Extract the ZIP file anywhere on your computer.
4. Open the extracted folder.

### Step 2: Open Terminal & Install Dependencies

Open your command prompt or terminal inside the extracted folder.

**Windows:**
Click the address bar in the folder, type `cmd`, and press Enter. Then run:
```bash
pip install -r requirements.txt
```

**macOS / Linux:**
Right-click the folder and select "New Terminal at Folder". Then run:
```bash
pip3 install -r requirements.txt
```

### Step 3: Run the Dashboard

```bash
python -m streamlit run streamlit_app.py
```

The dashboard will open automatically in your browser at:

```
http://localhost:8501
```

---

## 🎛️ Sidebar Filters

All filters are optional — leave empty to include all values:

| Filter | Options |
|---|---|
| 🌍 Region | Africa, Asia, Europe, North America, Oceania, South America |
| 📦 Subscription Type | Basic, Standard, Premium |
| 📱 Device | Desktop, Laptop, Mobile, TV, Tablet |
| 👤 Gender | Female, Male, Other |
| 🎭 Favorite Genre | Action, Comedy, Drama, Horror, Romance, Sci-Fi, Thriller |
| 📊 Customer Status | All / Active / Churned |

You can also **upload your own CSV** with the same column structure directly from the sidebar.

---

## 📁 Project Structure

```
streamlit_netflix_dashboard/
├── .streamlit/
│   └── config.toml          # Streamlit theme configuration (Dark Mode #07090E)
├── analysis.py               # 30 business questions logic & figure generation
├── DATASET_CARD.md           # Publication-ready Kaggle Dataset Card & Data Dictionary
├── dataset-metadata.json     # Kaggle API metadata descriptor
├── netflix_customer_churn.csv # Curated dataset (5,000 subscriber records)
├── netflix_logo.png          # Netflix brand header asset
├── netflix_n_transparent.png # Netflix icon asset
├── Netflix_done_.ipynb       # Original exploratory data analysis notebook
├── requirements.txt          # Python pinned dependencies
├── streamlit_app.py          # Executive multi-tab Streamlit application
├── test_analysis.py          # Validation test suite for all 30 analyses
├── .gitignore
└── README.md
```

---

## 📊 The 30 Business Questions

| # | Question |
|---|---|
| 1 | What is the average age of Netflix customers? |
| 2 | What is the average number of watch hours? |
| 3 | Who are the top 10 customers with the highest watch hours? |
| 4 | Which subscription type has the most customers? |
| 5 | Which region has the most customers? |
| 6 | Which device is used by the most customers? |
| 7 | Which payment method is used by the most customers? |
| 8 | Which favorite genre is the most popular? |
| 9 | Which gender group has the most customers? |
| 10 | Which subscription type has the highest average watch hours? |
| 11 | Which subscription type has the highest average watch time per day? |
| 12 | Which subscription type has the highest average monthly fee? |
| 13 | Which subscription type has the highest average number of profiles? |
| 14 | Which region has the highest average watch hours? |
| 15 | Which region has the highest average watch time per day? |
| 16 | Which device has the highest average watch hours? |
| 17 | Which favorite genre has the highest average watch hours? |
| 18 | Which payment method has the highest average watch hours? |
| 19 | What is the overall customer churn rate? |
| 20 | Which subscription type has the highest churn rate? |
| 21 | Which region has the highest churn rate? |
| 22 | Which device has the highest churn rate? |
| 23 | Which payment method has the highest churn rate? |
| 24 | Which favorite genre has the highest churn rate? |
| 25 | Which gender group has the highest churn rate? |
| 26 | What is the average watch hours for active and churned customers? |
| 27 | What is the average last login days for active and churned customers? |
| 28 | How many customers are active and how many have churned? |
| 29 | Which region-subscription combinations have the highest average watch hours? |
| 30 | Which subscription type has the highest total monthly fee value? |

---

## 🧪 Validate All 30 Analyses

Run the automated test suite anytime to verify all 30 questions:

```bash
python test_analysis.py
```

Expected output:
```
All 30 analyses, tables, texts, and visualizations passed successfully!
```

---

## 🌐 Kaggle Upload Guide

This dataset and codebase are fully configured for Kaggle:

1. **Via Kaggle Web UI:**
   - Go to [Kaggle New Dataset](https://www.kaggle.com/datasets/new).
   - Drag and drop `netflix_customer_churn.csv`.
   - Title: **Netflix Customer Churn & Engagement Analytics**.
   - Copy content from [`DATASET_CARD.md`](file:///DATASET_CARD.md) into the description.
2. **Via Kaggle CLI:**
   ```bash
   kaggle datasets create -p .
   ```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Streamlit** | Executive dark-themed interactive web dashboard |
| **Plotly** | Dynamic world choropleth map & interactive cards |
| **Pandas** | High-performance data manipulation & aggregation |
| **NumPy** | Statistical array benchmarks |
| **Matplotlib** | Visual charting for business question validation |

---

## 📝 License

This project and dataset are published under the **CC0 1.0 Universal (Public Domain)** license. Feel free to use, modify, and distribute for any educational, personal, or commercial portfolio project.

