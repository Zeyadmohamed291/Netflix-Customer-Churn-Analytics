"""Simple Pandas, NumPy, and Matplotlib analysis used by the Streamlit app."""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


EXPECTED_COLUMNS = [
    "customer_id",
    "age",
    "gender",
    "subscription_type",
    "watch_hours",
    "last_login_days",
    "region",
    "device",
    "monthly_fee",
    "churned",
    "payment_method",
    "number_of_profiles",
    "avg_watch_time_per_day",
    "favorite_genre",
]


QUESTIONS = {
    1: {
        "title_en": "What is the average age of Netflix customers?",
        "objective": "Calculate the average age across the selected customer segment.",
        "business_value": "Establishes a demographic baseline for audience targeting and content planning.",
    },
    2: {
        "title_en": "What is the average number of watch hours?",
        "objective": "Calculate the average watch hours across all selected customers.",
        "business_value": "Provides a simple benchmark for overall platform engagement.",
    },
    3: {
        "title_en": "Who are the top 10 customers with the highest watch hours?",
        "objective": "Rank customers by watch hours and return the top ten.",
        "business_value": "Identifies the most engaged customers for loyalty and retention programs.",
    },
    4: {
        "title_en": "Which subscription type has the most customers?",
        "objective": "Count customers within each subscription type.",
        "business_value": "Shows the most widely adopted plan and the current portfolio mix.",
    },
    5: {
        "title_en": "Which region has the most customers?",
        "objective": "Count customers in each geographic region.",
        "business_value": "Highlights the largest markets by customer volume.",
    },
    6: {
        "title_en": "Which device is used by the most customers?",
        "objective": "Count customers using each device category.",
        "business_value": "Helps prioritize product optimization for the most-used devices.",
    },
    7: {
        "title_en": "Which payment method is used by the most customers?",
        "objective": "Count customers by payment method.",
        "business_value": "Identifies the payment options that matter most to customers.",
    },
    8: {
        "title_en": "Which favorite genre is the most popular?",
        "objective": "Count customer preferences for each content genre.",
        "business_value": "Supports content investment and recommendation priorities.",
    },
    9: {
        "title_en": "Which gender group has the most customers?",
        "objective": "Measure the customer distribution across gender groups.",
        "business_value": "Provides a core demographic view of the customer base.",
    },
    10: {
        "title_en": "Which subscription type has the highest average watch hours?",
        "objective": "Compare average watch hours across subscription types.",
        "business_value": "Reveals which plan attracts the most engaged customers.",
    },
    11: {
        "title_en": "Which subscription type has the highest average watch time per day?",
        "objective": "Compare average daily watch time across subscription types.",
        "business_value": "Shows which plan is associated with stronger daily usage.",
    },
    12: {
        "title_en": "Which subscription type has the highest average monthly fee?",
        "objective": "Compare average monthly fees across subscription types.",
        "business_value": "Clarifies the pricing structure across the plan portfolio.",
    },
    13: {
        "title_en": "Which subscription type has the highest average number of profiles?",
        "objective": "Compare the average number of profiles across subscription types.",
        "business_value": "Helps explain household usage and account-sharing behavior.",
    },
    14: {
        "title_en": "Which region has the highest average watch hours?",
        "objective": "Compare average watch hours across geographic regions.",
        "business_value": "Identifies the markets with the strongest customer engagement.",
    },
    15: {
        "title_en": "Which region has the highest average watch time per day?",
        "objective": "Compare average daily watch time across regions.",
        "business_value": "Highlights differences in daily viewing behavior by market.",
    },
    16: {
        "title_en": "Which device has the highest average watch hours?",
        "objective": "Compare average watch hours across device categories.",
        "business_value": "Shows which device experience is linked to longer viewing sessions.",
    },
    17: {
        "title_en": "Which favorite genre has the highest average watch hours?",
        "objective": "Compare average watch hours by favorite genre.",
        "business_value": "Identifies the content preferences associated with deeper engagement.",
    },
    18: {
        "title_en": "Which payment method has the highest average watch hours?",
        "objective": "Compare average watch hours across payment methods.",
        "business_value": "Tests whether payment behavior is associated with different engagement levels.",
    },
    19: {
        "title_en": "What is the overall customer churn rate?",
        "objective": "Calculate the percentage of customers who have churned.",
        "business_value": "Provides the headline measure of the customer-retention challenge.",
    },
    20: {
        "title_en": "Which subscription type has the highest churn rate?",
        "objective": "Compare churn rates across subscription types.",
        "business_value": "Identifies the plan that requires the strongest retention action.",
    },
    21: {
        "title_en": "Which region has the highest churn rate?",
        "objective": "Compare churn rates across geographic regions.",
        "business_value": "Highlights markets that may need a localized retention strategy.",
    },
    22: {
        "title_en": "Which device has the highest churn rate?",
        "objective": "Compare churn rates across device categories.",
        "business_value": "Reveals whether a device experience may be linked to customer loss.",
    },
    23: {
        "title_en": "Which payment method has the highest churn rate?",
        "objective": "Compare churn rates across payment methods.",
        "business_value": "Can reveal payment friction or higher-risk customer segments.",
    },
    24: {
        "title_en": "Which favorite genre has the highest churn rate?",
        "objective": "Compare churn rates by favorite genre.",
        "business_value": "Connects content preference with customer-retention performance.",
    },
    25: {
        "title_en": "Which gender group has the highest churn rate?",
        "objective": "Compare churn rates across gender groups.",
        "business_value": "Shows whether retention performance differs across demographic segments.",
    },
    26: {
        "title_en": "What is the average watch hours for active and churned customers?",
        "objective": "Compare average watch hours for active and churned customers.",
        "business_value": "Tests whether lower engagement is associated with customer churn.",
    },
    27: {
        "title_en": "What is the average last login days for active and churned customers?",
        "objective": "Compare average days since last login for active and churned customers.",
        "business_value": "Shows how inactivity can act as an early churn warning signal.",
    },
    28: {
        "title_en": "How many customers are active and how many have churned?",
        "objective": "Count the exact number of active and churned customers.",
        "business_value": "Adds customer volume context to the churn percentage.",
    },
    29: {
        "title_en": "Which region-subscription combinations have the highest average watch hours?",
        "objective": "Rank region and subscription combinations by average watch hours.",
        "business_value": "Shows where each plan delivers its strongest engagement.",
    },
    30: {
        "title_en": "Which subscription type has the highest total monthly fee value?",
        "objective": "Sum monthly fee values for each subscription type.",
        "business_value": "Identifies the plan contributing the highest monthly value in the dataset.",
    },
}


QUESTION_CODE = {
    1: """average_age = np.mean(df['age'])\n\nprint(average_age)""",
    2: """average_watch_hours = np.mean(df['watch_hours'])\n\nprint(average_watch_hours)""",
    3: """top_10_customers = df.sort_values(\"watch_hours\", ascending=False).head(10)\n\nprint(top_10_customers[['customer_id', 'subscription_type', 'watch_hours']])""",
    4: """subscription_count = (\n    df.groupby(\"subscription_type\")['customer_id']\n    .count()\n    .sort_values(ascending=False)\n)\n\nprint(subscription_count)""",
    5: """region_count = (\n    df.groupby(\"region\")['customer_id']\n    .count()\n    .sort_values(ascending=False)\n)\n\nprint(region_count)""",
    6: """device_count = (\n    df.groupby(\"device\")['customer_id']\n    .count()\n    .sort_values(ascending=False)\n)\n\nprint(device_count)""",
    7: """payment_count = (\n    df.groupby(\"payment_method\")['customer_id']\n    .count()\n    .sort_values(ascending=False)\n)\n\nprint(payment_count)""",
    8: """genre_count = (\n    df.groupby(\"favorite_genre\")['customer_id']\n    .count()\n    .sort_values(ascending=False)\n)\n\nprint(genre_count)""",
    9: """gender_count = (\n    df.groupby(\"gender\")['customer_id']\n    .count()\n    .sort_values(ascending=False)\n)\n\nprint(gender_count)""",
    10: """subscription_watch = (\n    df.groupby(\"subscription_type\")['watch_hours']\n    .mean()\n    .sort_values(ascending=False)\n)\n\nprint(subscription_watch)""",
    11: """subscription_daily_watch = (\n    df.groupby(\"subscription_type\")['avg_watch_time_per_day']\n    .mean()\n    .sort_values(ascending=False)\n)\n\nprint(subscription_daily_watch)""",
    12: """subscription_fee = (\n    df.groupby(\"subscription_type\")['monthly_fee']\n    .mean()\n    .sort_values(ascending=False)\n)\n\nprint(subscription_fee)""",
    13: """subscription_profiles = (\n    df.groupby(\"subscription_type\")['number_of_profiles']\n    .mean()\n    .sort_values(ascending=False)\n)\n\nprint(subscription_profiles)""",
    14: """region_watch = (\n    df.groupby(\"region\")['watch_hours']\n    .mean()\n    .sort_values(ascending=False)\n)\n\nprint(region_watch)""",
    15: """region_daily_watch = (\n    df.groupby(\"region\")['avg_watch_time_per_day']\n    .mean()\n    .sort_values(ascending=False)\n)\n\nprint(region_daily_watch)""",
    16: """device_watch = (\n    df.groupby(\"device\")['watch_hours']\n    .mean()\n    .sort_values(ascending=False)\n)\n\nprint(device_watch)""",
    17: """genre_watch = (\n    df.groupby(\"favorite_genre\")['watch_hours']\n    .mean()\n    .sort_values(ascending=False)\n)\n\nprint(genre_watch)""",
    18: """payment_watch = (\n    df.groupby(\"payment_method\")['watch_hours']\n    .mean()\n    .sort_values(ascending=False)\n)\n\nprint(payment_watch)""",
    19: """churn_rate = df['churned'].mean() * 100\n\nprint(churn_rate)""",
    20: """subscription_churn = (\n    df.groupby(\"subscription_type\")['churned']\n    .mean() * 100\n)\n\nsubscription_churn = subscription_churn.sort_values(ascending=False)\nprint(subscription_churn)""",
    21: """region_churn = (\n    df.groupby(\"region\")['churned']\n    .mean() * 100\n)\n\nregion_churn = region_churn.sort_values(ascending=False)\nprint(region_churn)""",
    22: """device_churn = (\n    df.groupby(\"device\")['churned']\n    .mean() * 100\n)\n\ndevice_churn = device_churn.sort_values(ascending=False)\nprint(device_churn)""",
    23: """payment_churn = (\n    df.groupby(\"payment_method\")['churned']\n    .mean() * 100\n)\n\npayment_churn = payment_churn.sort_values(ascending=False)\nprint(payment_churn)""",
    24: """genre_churn = (\n    df.groupby(\"favorite_genre\")['churned']\n    .mean() * 100\n)\n\ngenre_churn = genre_churn.sort_values(ascending=False)\nprint(genre_churn)""",
    25: """gender_churn = (\n    df.groupby(\"gender\")['churned']\n    .mean() * 100\n)\n\ngender_churn = gender_churn.sort_values(ascending=False)\nprint(gender_churn)""",
    26: """watch_by_churn = (\n    df.groupby(\"churned\")['watch_hours']\n    .mean()\n    .sort_values(ascending=False)\n)\n\nprint(watch_by_churn)""",
    27: """login_by_churn = (\n    df.groupby(\"churned\")['last_login_days']\n    .mean()\n    .sort_values(ascending=False)\n)\n\nprint(login_by_churn)""",
    28: """churn_count = (\n    df.groupby(\"churned\")['customer_id']\n    .count()\n)\n\nprint(churn_count)""",
    29: """region_subscription_watch = (\n    df.groupby([\"region\", \"subscription_type\"])[\"watch_hours\"]\n    .mean()\n    .sort_values(ascending=False)\n    .head(10)\n)\n\nprint(region_subscription_watch)""",
    30: """total_fee_by_subscription = (\n    df.groupby(\"subscription_type\")['monthly_fee']\n    .sum()\n    .sort_values(ascending=False)\n)\n\nprint(total_fee_by_subscription)""",
}


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """Validate columns and apply only simple, course-level cleaning."""
    missing_columns = [column for column in EXPECTED_COLUMNS if column not in data.columns]
    if missing_columns:
        raise ValueError("Missing columns: " + ", ".join(missing_columns))

    df = data.loc[:, EXPECTED_COLUMNS].copy().drop_duplicates().dropna()

    numeric_columns = [
        "age",
        "watch_hours",
        "last_login_days",
        "monthly_fee",
        "churned",
        "number_of_profiles",
        "avg_watch_time_per_day",
    ]
    for column in numeric_columns:
        df.loc[:, column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna().copy()
    df.loc[:, "churned"] = df["churned"].astype(int)
    return df


def run_question(df: pd.DataFrame, number: int) -> Any:
    """Run one of the 30 analyses using the same simple code as the notebook."""
    if df.empty:
        raise ValueError("No rows are available after applying the filters.")

    if number == 1:
        return float(np.mean(df["age"]))
    if number == 2:
        return float(np.mean(df["watch_hours"]))
    if number == 3:
        return df.sort_values("watch_hours", ascending= False).head(10)[
            ["customer_id", "subscription_type", "watch_hours"]
        ]
    if number == 4:
        return df.groupby("subscription_type")["customer_id"].count().sort_values(ascending=False)
    if number == 5:
        return df.groupby("region")["customer_id"].count().sort_values(ascending=False)
    if number == 6:
        return df.groupby("device")["customer_id"].count().sort_values(ascending=False)
    if number == 7:
        return df.groupby("payment_method")["customer_id"].count().sort_values(ascending=False)
    if number == 8:
        return df.groupby("favorite_genre")["customer_id"].count().sort_values(ascending=False)
    if number == 9:
        return df.groupby("gender")["customer_id"].count().sort_values(ascending=False)
    if number == 10:
        return df.groupby("subscription_type")["watch_hours"].mean().sort_values(ascending=False)
    if number == 11:
        return df.groupby("subscription_type")["avg_watch_time_per_day"].mean().sort_values(ascending=False)
    if number == 12:
        return df.groupby("subscription_type")["monthly_fee"].mean().sort_values(ascending=False)
    if number == 13:
        return df.groupby("subscription_type")["number_of_profiles"].mean().sort_values(ascending=False)
    if number == 14:
        return df.groupby("region")["watch_hours"].mean().sort_values(ascending=False)
    if number == 15:
        return df.groupby("region")["avg_watch_time_per_day"].mean().sort_values(ascending=False)
    if number == 16:
        return df.groupby("device")["watch_hours"].mean().sort_values(ascending=False)
    if number == 17:
        return df.groupby("favorite_genre")["watch_hours"].mean().sort_values(ascending=False)
    if number == 18:
        return df.groupby("payment_method")["watch_hours"].mean().sort_values(ascending=False)
    if number == 19:
        return float(df["churned"].mean() * 100)
    if number == 20:
        return (df.groupby("subscription_type")["churned"].mean() * 100).sort_values(ascending=False)
    if number == 21:
        return (df.groupby("region")["churned"].mean() * 100).sort_values(ascending=False)
    if number == 22:
        return (df.groupby("device")["churned"].mean() * 100).sort_values(ascending=False)
    if number == 23:
        return (df.groupby("payment_method")["churned"].mean() * 100).sort_values(ascending=False)
    if number == 24:
        return (df.groupby("favorite_genre")["churned"].mean() * 100).sort_values(ascending=False)
    if number == 25:
        return (df.groupby("gender")["churned"].mean() * 100).sort_values(ascending=False)
    if number == 26:
        return df.groupby("churned")["watch_hours"].mean().sort_values(ascending=False)
    if number == 27:
        return df.groupby("churned")["last_login_days"].mean().sort_values(ascending=False)
    if number == 28:
        return df.groupby("churned")["customer_id"].count()
    if number == 29:
        return (
            df.groupby(["region", "subscription_type"])["watch_hours"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
        )
    if number == 30:
        return df.groupby("subscription_type")["monthly_fee"].sum().sort_values(ascending=False)

    raise ValueError("Question number must be between 1 and 30.")


def result_table(result: Any, number: int) -> pd.DataFrame:
    """Convert any result into a table suitable for Streamlit."""
    if isinstance(result, pd.DataFrame):
        return result.reset_index(drop=True)

    if isinstance(result, pd.Series):
        table = result.rename("value").reset_index()
        if number in (26, 27, 28):
            table = table.assign(
                churned=table["churned"].astype(str).map({"0": "Active", "1": "Churned"})
            )
        if number == 29:
            table.columns = ["region", "subscription_type", "value"]
        return table

    label = "percentage" if number == 19 else "value"
    return pd.DataFrame({label: [result]})


def main_result_text(result: Any, number: int) -> str:
    """Return the short headline answer shown above each result."""
    if number == 1:
        return f"Average customer age: {result:.2f} years"
    if number == 2:
        return f"Average watch hours: {result:.2f} hours"
    if number == 3:
        row = result.iloc[0]
        return f"Highest watch time: {row['watch_hours']:.2f} hours"
    if number == 19:
        return f"Overall churn rate: {result:.2f}%"
    if number == 28:
        active = int(result.get(0, 0))
        churned = int(result.get(1, 0))
        return f"Active customers: {active:,} | Churned customers: {churned:,}"
    if isinstance(result, pd.Series):
        top_label = result.index[0]
        top_value = result.iloc[0]
        if number in (26, 27):
            top_label = "Active (Non-churned)" if top_label == 0 else "Churned"
        elif isinstance(top_label, tuple):
            top_label = " + ".join(str(value) for value in top_label)
        suffix = "%" if number in range(20, 26) else ""
        unit = " hours" if number == 26 else (" days" if number == 27 else "")
        return f"Top result: {top_label} — {top_value:,.2f}{suffix}{unit}"
    return "The analysis was completed successfully."


def create_question_figure(df: pd.DataFrame, number: int, result: Any):
    """Create a simple Matplotlib figure for the selected question."""
    red = "#E50914"
    navy = "#0D1018"
    crimson = "#B20710"
    silver = "#CBD5E1"
    blue = "#3B82F6"
    green = "#22C55E"
    colors = ["#E50914", "#B20710", "#FFFFFF", "#CBD5E1", "#94A3B8", "#64748B", "#475569"]

    fig, ax = plt.subplots(figsize=(9, 4.6))
    fig.patch.set_facecolor("#0D1018")
    ax.set_facecolor("#0D1018")
    text_color = "#FFFFFF"
    muted_color = "#94A3B8"
    grid_color = "#1E2434"

    if number == 1:
        ax.hist(df["age"], bins=12, color=red, edgecolor="#0B0E14")
        ax.axvline(result, color=text_color, linestyle="--", linewidth=2, label=f"Average = {result:.2f}")
        ax.set_title("Customer Age Distribution", color=text_color, fontweight="bold")
        ax.set_xlabel("Age", color=muted_color)
        ax.set_ylabel("Number of Customers", color=muted_color)
        ax.legend(facecolor="#141820", edgecolor=grid_color, labelcolor=text_color)
    elif number == 2:
        ax.hist(df["watch_hours"], bins=14, color=blue, edgecolor="#0B0E14")
        ax.axvline(result, color=red, linestyle="--", linewidth=2, label=f"Average = {result:.2f}")
        ax.set_title("Watch Hours Distribution", color=text_color, fontweight="bold")
        ax.set_xlabel("Watch Hours", color=muted_color)
        ax.set_ylabel("Number of Customers", color=muted_color)
        ax.legend(facecolor="#141820", edgecolor=grid_color, labelcolor=text_color)
    elif number == 3:
        chart_data = result.sort_values("watch_hours")
        labels = chart_data["customer_id"].str[:8]
        ax.barh(labels, chart_data["watch_hours"], color=red)
        ax.set_title("Top 10 Customers by Watch Hours", color=text_color, fontweight="bold")
        ax.set_xlabel("Watch Hours", color=muted_color)
        ax.set_ylabel("Customer ID", color=muted_color)
    elif number in (19, 28):
        counts = df.groupby("churned")["customer_id"].count().reindex([0, 1], fill_value=0)
        ax.pie(
            counts.values,
            labels=["Active", "Churned"],
            autopct="%1.1f%%",
            startangle=90,
            colors=[green, red],
            wedgeprops={"edgecolor": "#0B0E14", "linewidth": 2},
            textprops={"color": text_color, "fontweight": "bold"},
        )
        ax.set_title("Active vs Churned Customers", color=text_color, fontweight="bold")
    elif number == 29:
        chart_data = result.sort_values()
        labels = [f"{region} | {subscription}" for region, subscription in chart_data.index]
        ax.barh(labels, chart_data.values, color=blue)
        ax.set_title("Top Region and Subscription Combinations", color=text_color, fontweight="bold")
        ax.set_xlabel("Average Watch Hours", color=muted_color)
    else:
        chart_data = result.copy()
        if number in (26, 27):
            chart_data.index = chart_data.index.map({0: "Active", 1: "Churned"})
        chart_data.plot(kind="bar", ax=ax, color=colors[: len(chart_data)], width=0.72)
        ax.set_title(QUESTIONS[number]["title_en"], color=text_color, fontweight="bold")
        ax.set_xlabel("")
        if number in range(20, 26):
            ax.set_ylabel("Churn Rate (%)", color=muted_color)
        elif number in (4, 5, 6, 7, 8, 9):
            ax.set_ylabel("Number of Customers", color=muted_color)
        elif number == 30:
            ax.set_ylabel("Total Monthly Fee", color=muted_color)
        else:
            ax.set_ylabel("Average Value", color=muted_color)
        ax.tick_params(axis="x", rotation=25)

    ax.tick_params(colors=muted_color)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(grid_color)
    ax.spines["left"].set_color(grid_color)
    ax.grid(axis="y", alpha=0.1, color=muted_color)
    fig.tight_layout()
    return fig
