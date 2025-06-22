import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from scipy.stats import chi2_contingency

# Set style for plots
plt.style.use("seaborn-v0_8")
sns.set_theme()


def load_and_preprocess_data(file_path):
    """
    Load and preprocess the hotel reservations dataset
    """
    # Load the dataset
    df = pd.read_csv(file_path)

    # Handle missing values
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=["object"]).columns

    for col in numerical_cols:
        df[col] = df[col].fillna(df[col].mean())

    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    # Convert date columns if present
    if "arrival_date" in df.columns:
        df["arrival_date"] = pd.to_datetime(df["arrival_date"])
        df["arrival_month"] = df["arrival_date"].dt.month
        df["arrival_year"] = df["arrival_date"].dt.year

    return df


def analyze_cancellation_by_country(df):
    """
    Analyze cancellation patterns by country with improved visualization
    """
    # Calculate cancellation rates by country
    country_stats = (
        df.groupby("country")
        .agg({"is_canceled": ["count", "mean"], "lead_time": "mean"})
        .reset_index()
    )
    country_stats.columns = ["country", "booking_count", "cancel_rate", "avg_lead_time"]

    # Filter countries with at least 10 bookings
    country_stats = country_stats[country_stats["booking_count"] >= 10]
    country_stats = country_stats.sort_values("cancel_rate", ascending=False)

    # Prepare data for visualization
    top_6 = country_stats.head(6)
    other_sample = country_stats.iloc[6:16]  # Next 10 countries for comparison

    # Create visualization
    plt.figure(figsize=(15, 8))
    bars = plt.bar(
        range(16),
        list(top_6["cancel_rate"]) + list(other_sample["cancel_rate"]),
        color=["red" if i < 6 else "gray" for i in range(16)],
    )

    # Customize the plot
    plt.title(
        "Top 6 Countries with Highest Cancellation Rates\n(Compared with Next 10 Countries)",
        pad=20,
    )
    plt.xlabel("Countries")
    plt.ylabel("Cancellation Rate")
    plt.xticks(
        range(16),
        list(top_6["country"]) + list(other_sample["country"]),
        rotation=45,
        ha="right",
    )

    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        bookings = (
            top_6["booking_count"].iloc[i]
            if i < 6
            else other_sample["booking_count"].iloc[i - 6]
        )
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"Rate: {height:.2f}\nBookings: {bookings}",
            ha="center",
            va="bottom",
        )

    plt.tight_layout()
    plt.savefig("cancellation_by_country.png", dpi=300, bbox_inches="tight")
    plt.close()

    return top_6, other_sample


def calculate_cramers_v(confusion_matrix):
    """
    Calculate Cramer's V statistic for categorical-categorical association.
    """
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    min_dim = min(confusion_matrix.shape) - 1
    return np.sqrt(chi2 / (n * min_dim))


def analyze_key_attributes(df):
    """
    Identify key attributes contributing to cancellations with improved visualization
    """
    # Calculate correlations for numerical features
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    correlations = df[numerical_cols].corr()["is_canceled"].sort_values(ascending=False)

    # Calculate Cramer's V for categorical features
    categorical_cols = df.select_dtypes(include=["object"]).columns
    cramers_v_scores = {}
    for col in categorical_cols:
        confusion_matrix = pd.crosstab(df[col], df["is_canceled"])
        cramers_v_scores[col] = calculate_cramers_v(confusion_matrix)

    # Combine all features and their importance scores
    feature_importance = pd.DataFrame(
        {
            "Feature": list(correlations.index) + list(cramers_v_scores.keys()),
            "Score": list(correlations.values) + list(cramers_v_scores.values()),
            "Type": [
                "Correlation" if x in correlations.index else "Cramer's V"
                for x in list(correlations.index) + list(cramers_v_scores.keys())
            ],
        }
    )

    # Sort by absolute value of score
    feature_importance["Abs_Score"] = abs(feature_importance["Score"])
    feature_importance = feature_importance.sort_values("Abs_Score", ascending=False)

    # Remove self-correlation and obvious features
    feature_importance = feature_importance[
        ~feature_importance["Feature"].isin(
            ["is_canceled", "reservation_status", "reservation_status_date"]
        )
    ]

    # Plot top 10 most important features
    plt.figure(figsize=(12, 8))
    colors = [
        (
            "red"
            if x
            in ["lead_time", "deposit_type", "previous_cancellations", "market_segment"]
            else "lightgray"
        )
        for x in feature_importance["Feature"][:10]
    ]

    bars = plt.barh(range(10), feature_importance["Abs_Score"][:10], color=colors)
    plt.yticks(range(10), feature_importance["Feature"][:10])

    # Add score labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(
            width,
            bar.get_y() + bar.get_height() / 2.0,
            f'{feature_importance["Score"].iloc[i]:.3f} ({feature_importance["Type"].iloc[i]})',
            ha="left",
            va="center",
            fontsize=10,
        )

    plt.title(
        "Top 10 Features Contributing to Cancellation\n(Red: Key Predictors)", pad=20
    )
    plt.xlabel("Absolute Score (Correlation or Cramer's V)")

    plt.tight_layout()
    plt.savefig("feature_importance.png", dpi=300, bbox_inches="tight")
    plt.close()

    return feature_importance


def analyze_lead_time(df):
    """
    Analyze the relationship between lead time and cancellations
    """
    # Create lead time categories
    df["lead_time_category"] = pd.qcut(
        df["lead_time"],
        q=5,
        labels=["Very Short", "Short", "Medium", "Long", "Very Long"],
    )

    # Calculate correlation coefficient
    lead_time_correlation = df["lead_time"].corr(df["is_canceled"])

    # Calculate cancellation rates by lead time category
    lead_time_analysis = (
        df.groupby("lead_time_category", observed=True)["is_canceled"]
        .agg(["mean", "count", lambda x: np.std(x) / np.sqrt(len(x))])  # Standard error
        .rename(columns={"mean": "cancel_rate", "<lambda_0>": "std_error"})
    )

    # Plot cancellation rate by lead time category with error bars
    plt.figure(figsize=(10, 6))
    bars = plt.bar(
        range(5),
        lead_time_analysis["cancel_rate"],
        yerr=lead_time_analysis["std_error"],
        capsize=5,
        color="lightblue",
        edgecolor="black",
    )

    # Add value labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        count = lead_time_analysis["count"].iloc[i]
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"Rate: {height:.3f}\nN: {count}",
            ha="center",
            va="bottom",
        )

    plt.title(
        f"Cancellation Rate by Lead Time\nCorrelation: {lead_time_correlation:.3f}"
    )
    plt.xlabel("Lead Time Category")
    plt.ylabel("Cancellation Rate")
    plt.xticks(range(5), lead_time_analysis.index, rotation=45)

    plt.tight_layout()
    plt.savefig("lead_time_analysis.png", dpi=300, bbox_inches="tight")
    plt.close()

    return lead_time_analysis, lead_time_correlation


def main():
    # Load and preprocess data
    df = load_and_preprocess_data("../data/hotel-reservations.csv")

    # Perform analyses
    top_countries, other_countries = analyze_cancellation_by_country(df)
    feature_importance = analyze_key_attributes(df)
    lead_time_analysis, lead_time_corr = analyze_lead_time(df)

    # Print summary statistics
    print("\nTop 6 Countries with Highest Cancellation Rates:")
    print(top_countries[["country", "cancel_rate", "booking_count"]])

    print("\nFeature Importance Summary:")
    print(feature_importance.head(10))

    print("\nLead Time Impact on Cancellations:")
    print(f"Correlation coefficient: {lead_time_corr:.3f}")
    print(lead_time_analysis)


if __name__ == "__main__":
    main()
