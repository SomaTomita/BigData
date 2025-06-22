import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

from sklearn.model_selection import KFold, cross_val_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

# ---------- 0. configuration ----------
DATA_DIR = Path("../data")
TRAIN_CSV = DATA_DIR / "apartment_for_rent_train.csv"
TEST_CSV = DATA_DIR / "apartment_for_rent_test.csv"
RANDOM_SEED = 42
PLOTS_DIR = Path("plots")
PLOTS_DIR.mkdir(exist_ok=True)


# ---------- 1. utility: canonical mappers ----------
BALCONY_MAP = {
    "closed balcony": "Closed balcony",
    "closed_balcony": "Closed balcony",
    "closed": "Closed balcony",
    "open balcony": "Open balcony",
    "open_balcony": "Open balcony",
    "open": "Open balcony",
    "multiple balconies": "Multiple balconies",
    "multiple_balconies": "Multiple balconies",
    "multible": "Multiple balconies",
    "0": "Not available",
    "none": "Not available",
    "nan": "Not available",
    "": "Not available",
    "not available": "Not available",
    "not_available": "Not available",
}
CONSTRUCTION_MAP = {"monolith": "Monolith", "stone": "Stone", "panels": "Panels", "bricks": "Bricks"}
FURNITURE_MAP = {
    "available": "Available",
    "by agreement": "By agreement",
    "partial furniture": "Partial",
    "not available": "Not available",
    "": "Unknown",
    "nan": "Unknown",
    "none": "Unknown",
}
# This should be updated with the latest exchange rates
CURRENCY_RATES = {
    "AMD": 0.0026,
    "USD": 1.0,
    "RUB": 0.011,
    "EUR": 1.07,
}
BOOL_COLS = ["New_construction", "Elevator"]
NUM_COLS = [
    "Number_of_rooms",
    "Number_of_bathrooms",
    "Floor_area",
    "Ceiling_height",
    "Floors_in_the_building",
    "Floor",
]
CAT_COLS = [
    "Balcony",
    "Furniture",
    "Renovation",
    "Children_are_welcome",
    "Pets_allowed",
    "Utility_payments",
    "Construction_type",
]
CITY_MAP = {
    "Yerevan": "Yerevan",
    "Երևան": "Yerevan",
    "Ереван": "Yerevan",
    "Artashat": "Artashat",
    "Echmiadzin": "Echmiadzin",
    "Vardenis": "Vardenis",
    "Tsaghkadzor": "Tsaghkadzor",
    "Gyumri": "Gyumri",
    "Dilijan": "Dilijan",
}


def extract_city(address: str) -> str:
    """Extract city name from address string."""
    if pd.isna(address) or not isinstance(address, str) or not address.strip():
        return "Unknown"
    # Split address and check each part
    parts = address.split("›")
    if len(parts) > 1:
        city_part = parts[-1].strip()
    else:
        # Try to extract from comma-separated format
        parts = address.split(",")
        city_part = parts[-1].strip()
    # Add empty string check
    if not city_part:
        return "Unknown"
    # Clean and map city names
    try:
        city = city_part.split()[0]  # Take first word
        return CITY_MAP.get(city, "Other")
    except (IndexError, AttributeError):
        return "Unknown"


# ---------- 1. common utility ----------
def load_and_prepare(train_path: Path, test_path: Path):
    """Load CSV, clean basic issues, and prepare data for modeling."""
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)

    # --- realign the test set: insert the three missing columns and shift everything right ---
    train_cols = train.columns.tolist()
    miss_cols = ["Reg_id", "Gender", "Age"]
    new_test = pd.DataFrame(columns=train_cols)
    # add empty columns for the gap
    for col in miss_cols:
        if col not in test.columns:
            new_test[col] = np.nan
    # copy test values to correct positions
    for i, col in enumerate(test.columns):
        if i < len(train_cols):
            new_test[train_cols[i]] = test[col]
    # replace mis-aligned test
    test = new_test
    # --- drop the three personal columns (not used in Task 1) ---
    train = train.drop(columns=miss_cols)
    test = test.drop(columns=miss_cols)

    # --- keep only columns common to both splits ---
    common = list(set(train.columns) & set(test.columns))
    X = train[common].copy()
    X_test = test[common].copy()

    # Clean both datasets
    for df in (X, X_test):
        # Balcony standardization
        df["Balcony"] = df["Balcony"].astype(str).str.strip().str.lower().replace(BALCONY_MAP).fillna("Not available")
        # Furniture standardization
        df["Furniture"] = df["Furniture"].astype(str).str.strip().str.lower().replace(FURNITURE_MAP).fillna("Unknown")
        # Construction and Renovation handling
        df["Construction_type"] = (
            df["Construction_type"].fillna("Unknown").astype(str).str.strip().str.lower().replace(CONSTRUCTION_MAP)
        )
        df["Renovation"] = df["Renovation"].fillna("Unknown").astype(str).str.strip().str.replace("_", " ").str.title()

        # Boolean columns
        for col in BOOL_COLS:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
        # Numeric columns with sanity limits
        df[NUM_COLS] = df[NUM_COLS].apply(pd.to_numeric, errors="coerce")
        df["Floors_in_the_building"] = df["Floors_in_the_building"].clip(lower=0)
        df["Floor_area"] = df["Floor_area"].clip(lower=20, upper=1000)

        # Calculate monthly price in USD
        df["Duration_days"] = df["Duration"].str.lower().map({"daily": 1, "monthly": 30}).fillna(30).astype(int)
        df["Price_usd_month"] = (
            df["Price"] * df["Currency"].map(CURRENCY_RATES).fillna(1.0) * (30 / df["Duration_days"])
        )

        # Address processing
        if "Address" in df.columns:
            df["City"] = df["Address"].apply(extract_city)

        # Categorical columns with simple numeric encoding
        for col in ["Children_are_welcome", "Pets_allowed", "Utility_payments"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
                df[col] = df[col].map({0: "No"}).fillna("Yes")
                df.loc[df[col].isna(), col] = "Unknown"

    # Extract target and drop unnecessary columns
    y = X["Price_usd_month"]
    drop_cols = [
        "Price",
        "Price_usd",
        "Duration",
        "Duration_days",
        "Currency",
        "Address",
        "Datetime",
        "amenities",
        "appliances",
        "parking",
    ]
    X = X.drop(columns=[c for c in drop_cols if c in X.columns])

    # Filter valid prices and reset index
    mask = y.notna() & y.between(50, 10000)
    return X.loc[mask].reset_index(drop=True), y[mask].reset_index(drop=True), X_test


X_train, y_train, X_test = load_and_prepare(TRAIN_CSV, TEST_CSV)


# def check_data_quality(X: pd.DataFrame, y: pd.Series):
#     """Check data quality and print detailed information."""
#     print("=== Data Quality Check ===")
#     print(f"X shape: {X.shape}")
#     print(f"y shape: {y.shape}")
#     print(f"X columns: {list(X.columns)}")
#     print(f"y name: {y.name}")

#     # Check missing values
#     print(f"\nMissing values in X:")
#     missing_X = X.isnull().sum()
#     print(missing_X[missing_X > 0])

#     print(f"\nMissing values in y: {y.isnull().sum()}")

#     # Price analysis for setting bounds
#     print(f"\n=== Price Analysis for Bounds Setting ===")
#     print(f"Price statistics:")
#     print(y.describe())

#     # Analyze price distribution for reasonable bounds
#     print(f"\nPrice percentiles:")
#     percentiles = [0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
#     for p in percentiles:
#         print(f"  {p*100:2.0f}%: ${y.quantile(p):.0f}")

#     # Currency distribution
#     if "Currency" in X.columns:
#         print(f"\nCurrency distribution:")
#         print(X["Currency"].value_counts())

#     # Suggest reasonable bounds
#     print(f"\n=== Suggested Price Bounds ===")
#     print(f"Current range: ${y.min():.0f} - ${y.max():.0f}")
#     print(f"Suggested minimum: $10 (reasonable for daily rental)")
#     print(f"Suggested maximum: $10,000 (reasonable for luxury apartment)")
#     print(f"Data points outside suggested bounds: {((y < 10) | (y > 10000)).sum()}")

#     # Basic statistics
#     print(f"\nX info:")
#     print(X.info())
#     print(f"\ny info:")
#     print(y.describe())

#     # Data integrity check
#     if len(X) != len(y):
#         print("ERROR: X and y have different lengths!")
#         return False

#     if y.isnull().any():
#         print("ERROR: y contains missing values!")
#         return False

#     return True


# if not check_data_quality(X_train, y_train):
#     raise ValueError("Data quality check failed!")


# =========================================================
# Task a – three discrete variables most linked to high price
# =========================================================
def task_a_discrete_vars(X: pd.DataFrame, y: pd.Series):
    """Identify top-3 categorical features driving price."""
    # Combine rare categories
    for col in CAT_COLS:
        counts = X[col].value_counts()
        rare_categories = counts[counts < 50].index
        X[col] = X[col].replace(rare_categories, "Other")

    scores = {}
    eta_squared = {}
    for col in CAT_COLS:
        groups = []
        for value in X[col].unique():
            if pd.isna(value):
                continue
            group_data = y[X[col] == value]
            if len(group_data) >= 5:  # Minimum 5 samples
                groups.append(group_data.values)

        if len(groups) >= 2:
            try:
                if len(groups) == 2:  # binary → Welch t
                    t, p = stats.ttest_ind(*groups, equal_var=False)
                    f_stat = t**2
                else:  # ≥3 → one-way ANOVA
                    f_stat, p = stats.f_oneway(*groups)
                scores[col] = (f_stat, p)

                # Calculate η²
                ss_between = sum(len(g) * (g.mean() - y.mean()) ** 2 for g in groups)
                ss_total = sum((y - y.mean()) ** 2)
                eta_squared[col] = ss_between / ss_total
            except Exception:
                continue

    top3 = sorted(scores.items(), key=lambda x: x[1][0], reverse=True)[:3]

    # Log transformation and ANOVA
    y_log = np.log1p(y)
    log_scores = {}
    for col in CAT_COLS:
        groups = []
        for value in X[col].unique():
            if pd.isna(value):
                continue
            group_data = y_log[X[col] == value]
            if len(group_data) >= 5:  # Minimum 5 samples
                groups.append(group_data.values)

        if len(groups) >= 2:
            try:
                if len(groups) == 2:  # binary → Welch t
                    t, p = stats.ttest_ind(*groups, equal_var=False)
                    f_stat = t**2
                else:  # ≥3 → one-way ANOVA
                    f_stat, p = stats.f_oneway(*groups)
                log_scores[col] = (f_stat, p)
            except Exception:
                continue

    # Create plots
    for col, (f_stat, p_val) in top3:
        data = pd.DataFrame({col: X[col], "Price": y})
        cat_means = data.groupby(col)["Price"].mean().sort_values(ascending=False)
        order = cat_means.index.tolist()

        plt.figure(figsize=(10, 6))
        sns.boxplot(x=col, y="Price", data=data, order=order, width=0.5)
        sample_data = data.sample(min(1000, len(data)))
        sns.swarmplot(x=col, y="Price", data=sample_data, order=order, size=1, alpha=0.2, color="black")

        for i, category in enumerate(order):
            n = len(data[data[col] == category])
            plt.text(i, plt.ylim()[1], f"N={n}", ha="center", va="bottom")

        plt.title(f"Price distribution by {col}\n(F={f_stat:.1f}, p={p_val:.3f}, η²={eta_squared[col]:.3f})", pad=20)
        plt.xlabel(col)
        plt.ylabel("Monthly rental price (USD)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(PLOTS_DIR / f"a_box_{col}.png", dpi=300, bbox_inches="tight")
        plt.close()

    return top3, eta_squared, log_scores


top3_discrete, eta_squared, log_scores = task_a_discrete_vars(X_train, y_train)


# =========================================================
# Task b – correlation between rooms, price, duration
# =========================================================
def task_b_correlation(X: pd.DataFrame, y: pd.Series):
    """Compute correlations between rooms and price with improved visualization."""
    subset = pd.DataFrame({"Rooms": X["Number_of_rooms"], "Price": y})
    subset["LogPrice"] = np.log1p(subset["Price"])
    N = len(subset)

    # Calculate correlation matrices for both raw and log-transformed prices
    corr_p = subset[["Rooms", "Price", "LogPrice"]].corr(method="pearson")
    corr_s = subset[["Rooms", "Price", "LogPrice"]].corr(method="spearman")

    # Scatter plot with log-transformed price
    plt.figure(figsize=(10, 6))
    sns.regplot(
        data=subset,
        x="Rooms",
        y="LogPrice",
        scatter_kws={"alpha": 0.3, "s": 10},
        line_kws={"color": "red"},
    )
    r_p = corr_p.loc["Rooms", "LogPrice"]
    r_s = corr_s.loc["Rooms", "LogPrice"]
    plt.text(
        0.05,
        0.95,
        f"Pearson (ρ) = {r_p:.2f}\nSpearman (ρₛ) = {r_s:.2f}",
        transform=plt.gca().transAxes,
        bbox=dict(facecolor="white", alpha=0.8),
        verticalalignment="top",
    )
    plt.xlabel("Number of rooms")
    plt.ylabel("Log Monthly rental price (log1p USD)")
    plt.title(f"Log-Price vs Rooms correlation (N={N})")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "b_scatter_pair.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Box plot for price distribution by room count
    plt.figure(figsize=(12, 6))
    room_counts = subset["Rooms"].value_counts()
    valid_rooms = room_counts[room_counts >= 10].index.sort_values()
    sns.boxplot(data=subset[subset["Rooms"].isin(valid_rooms)], x="Rooms", y="Price")
    plt.title("Price distribution by number of rooms")
    plt.xlabel("Number of rooms")
    plt.ylabel("Monthly rental price (USD)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "b_box_rooms.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        corr_p[["Price", "LogPrice"]].loc[["Rooms", "Price", "LogPrice"]],
        annot=True,
        cmap="Blues",
        vmin=-1,
        vmax=1,
        square=True,
        fmt=".2f",
    )
    plt.title(f"Correlation matrix (N={N})")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "b_corr_dual.png", dpi=300, bbox_inches="tight")
    plt.close()

    return corr_p, corr_s


corr_pearson, corr_spearman = task_b_correlation(X_train, y_train)


# =========================================================
# Task c – address significance + three further attributes
# =========================================================
def task_c_address_and_features(X: pd.DataFrame):
    """Analyze address significance and identify key price predictors."""
    y = X["Price_usd_month"]
    X = X.drop(columns=["Price_usd_month"])
    model_cols = X.columns.tolist()

    # Preprocessing
    numeric_pipe = Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())])
    cat_pipe = Pipeline(
        [("imp", SimpleImputer(strategy="most_frequent")), ("ohe", OneHotEncoder(handle_unknown="ignore"))]
    )
    num_cols = [c for c in model_cols if c in NUM_COLS]
    cat_cols = [c for c in model_cols if c not in num_cols]
    preproc = ColumnTransformer([("num", numeric_pipe, num_cols), ("cat", cat_pipe, cat_cols)])

    # Single-threaded trees + lighter forest
    model = Pipeline(
        [("prep", preproc), ("rf", RandomForestRegressor(n_estimators=20, random_state=RANDOM_SEED, n_jobs=1))]
    )
    # 3-fold cross-validation with parallel processing
    cv = KFold(n_splits=3, shuffle=True, random_state=RANDOM_SEED)
    rmse = -cross_val_score(model, X, y, cv=cv, scoring="neg_root_mean_squared_error", n_jobs=-1).mean()

    # Fit & feature importance
    model.fit(X, y)
    feature_names = model.named_steps["prep"].get_feature_names_out()
    importances = pd.Series(model.named_steps["rf"].feature_importances_, index=feature_names)
    top3_features = importances.sort_values(ascending=False).head(3)

    # Plot feature importance
    plt.figure(figsize=(10, 6))
    importances.sort_values(ascending=True).tail(10).plot(kind="barh")
    plt.title("Top 10 Feature Importance")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "c_feature_importance.png")
    plt.close()

    # Scatter plots for numeric features
    for col in num_cols:
        if col in X.columns:  # Only plot if feature wasn't one-hot encoded
            plt.figure(figsize=(6, 4))
            sns.regplot(data=X, x=col, y=y, scatter_kws={"alpha": 0.5})
            plt.title(f"{col} vs Monthly Price (USD)")
            plt.tight_layout()
            plt.savefig(PLOTS_DIR / f"c_scatter_{col}.png")
            plt.close()

    return rmse, top3_features


rmse, top3_features = task_c_address_and_features(X_train)


# ---------- **console summary** ----------
def print_section_header(title):
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")


def print_correlation_matrix(matrix, title):
    print(f"\n{title}:")
    # Display with 2 decimal places and format the matrix
    pd.set_option("display.precision", 2)
    pd.set_option("display.max_columns", None)
    print(matrix.round(2).to_string())


# Task A Summary
print_section_header("TASK A: Top Discrete Variables Analysis")
for var, (f_stat, p_val) in top3_discrete:
    significance = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else "ns"
    print(f"{var:<20} F={f_stat:>8.1f}  p={p_val:.3e} {significance}")

# Task B Summary
print_section_header("TASK B: Correlation Analysis")
print_correlation_matrix(corr_pearson, "Pearson Correlations")
print_correlation_matrix(corr_spearman, "Spearman Correlations")

# Task C Summary
print_section_header("TASK C: Address and Feature Importance")
print(f"\nModel Performance:")
print(f"  • RMSE:            ${rmse:>8,.0f}")

print("\nTop 3 features:")
for name, importance in top3_features.items():
    print(f"{name:<30} {importance:.3f}")
