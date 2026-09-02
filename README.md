# 🎬 Netflix Customer Churn Analytics Dashboard

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.62-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.2-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.10-11557C?style=for-the-badge&logo=python&logoColor=white)

**A professional, dark-themed interactive dashboard for exploring Netflix customer churn data — featuring 30 business questions with full code, results, and visualizations.**

</div>

---

## 📸 Dashboard Preview

| Feature | Description |
|---------|-------------|
| 🏠 **Executive Overview** | Headline KPIs, customer status donut chart, largest market & plan |
| 👥 **Customer Analytics** | Distribution by region, device, subscription type & favorite genre |
| 📉 **Churn Analysis** | Churn rates by subscription, region, device, payment & engagement |
| ❓ **30 Business Questions** | Each with objective, business value, Python code, result table & chart |
| 🗃️ **Data Explorer** | Filtered records, statistics, data quality metrics & CSV export |

---

## 🚀 Quick Start (Setup on Any Computer)

### Prerequisites

- **Python 3.10+** installed — [Download Python](https://www.python.org/downloads/)
- **Git** installed — [Download Git](https://git-scm.com/downloads)

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### Step 2: Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Dashboard

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
|--------|---------|
| 🌍 Region | Africa, Asia, Europe, North America, Oceania, South America |
| 📦 Subscription Type | Basic, Standard, Premium |
| 📱 Device | Desktop, Laptop, Phone, Smart TV, Tablet |
| 👤 Gender | Female, Male, Other |
| 🎭 Favorite Genre | Action, Comedy, Drama, Horror, Romance, Sci-Fi, Thriller |
| 📊 Customer Status | All / Active / Churned |

You can also **upload your own CSV** with the same column structure.

---

## 📁 Project Structure

```
streamlit_netflix_dashboard/
├── .streamlit/
│   └── config.toml          # Streamlit theme configuration
├── analysis.py               # 30 business questions logic & chart generation
├── netflix_customer_churn.csv # Dataset (5,000 customers)
├── streamlit_app.py           # Main dashboard application
├── requirements.txt           # Python dependencies
├── test_analysis.py           # Validation script for all 30 analyses
├── Netflix_done_.ipynb        # Original Jupyter Notebook
├── .gitignore
└── README.md
```

---

## 📊 The 30 Business Questions

| # | Question |
|---|----------|
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

```bash
python test_analysis.py
```

Expected output:
```
All 30 analyses passed.
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Interactive web dashboard |
| **Pandas** | Data manipulation & analysis |
| **NumPy** | Numerical computations |
| **Matplotlib** | Data visualization & charts |

---

## 📝 License

This project is for educational purposes.
