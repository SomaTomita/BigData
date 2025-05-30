import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


# Custom metrics to match WEKA's metrics
def root_relative_squared_error(y_true, y_pred):
    numerator = np.sum((y_true - y_pred) ** 2)
    denominator = np.sum((y_true - np.mean(y_true)) ** 2)
    return np.sqrt(numerator / denominator)


def relative_absolute_error(y_true, y_pred):
    numerator = np.sum(np.abs(y_true - y_pred))
    denominator = np.sum(np.abs(y_true - np.mean(y_true)))
    return numerator / denominator


# Load and prepare data
possum_data = pd.read_csv(
    "../../Week3-Statistics-and-MachineLearning/activity-LinearRegression/possum.csv"
)
possum_encoded = pd.get_dummies(possum_data)

# Select features and target
features_data = possum_encoded[
    ["site", "age", "headL", "skullW ", "totalL", "sex_m", "sex_f"]
]
target_data = possum_encoded["tailL"]

# First experiment: Using all data
print("============= Using All Data =============")
X_train, X_test = features_data, features_data
y_train, y_test = target_data, target_data

# Linear Regression
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_pred = lr_model.predict(X_test)

# SVR with scaling
feature_scaler = StandardScaler()
X_train_scaled = feature_scaler.fit_transform(X_train)
target_scaler = StandardScaler()
y_train_scaled = target_scaler.fit_transform(y_train.values.reshape(-1, 1))

svr_model = SVR(kernel="rbf", C=1.0, epsilon=0.1)
svr_model.fit(X_train_scaled, np.reshape(y_train_scaled, -1))
svr_pred = svr_model.predict(feature_scaler.transform(X_test))
svr_pred = target_scaler.inverse_transform(svr_pred.reshape(-1, 1)).flatten()

# Print results for full dataset
print("---------------- Linear Regression Model -----------------------------")
print(f"RRSE: {root_relative_squared_error(y_test, lr_pred):.3f}")
print(f"RAE: {relative_absolute_error(y_test, lr_pred):.3f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, lr_pred)):.3f}")
print(f"R² score: {r2_score(y_test, lr_pred):.3f}")
print(f"MAE: {mean_absolute_error(y_test, lr_pred):.3f}")

print("\n---------------- SVR Model -----------------------------")
print(f"RRSE: {root_relative_squared_error(y_test, svr_pred):.3f}")
print(f"RAE: {relative_absolute_error(y_test, svr_pred):.3f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, svr_pred)):.3f}")
print(f"R² score: {r2_score(y_test, svr_pred):.3f}")
print(f"MAE: {mean_absolute_error(y_test, svr_pred):.3f}")

# Second experiment: Percentage splits
print("\n============= Percentage Split Experiments =============")
split_sizes = [0.2, 0.3, 0.4, 0.5]

for size in split_sizes:
    print(f"\n######### Percentage Split: {int(size*100)}% #########")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        features_data, target_data, test_size=size, random_state=19
    )

    # Linear Regression
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    lr_pred = lr_model.predict(X_test)

    # SVR with scaling
    feature_scaler = StandardScaler()
    X_train_scaled = feature_scaler.fit_transform(X_train)
    target_scaler = StandardScaler()
    y_train_scaled = target_scaler.fit_transform(y_train.values.reshape(-1, 1))

    svr_model = SVR(kernel="rbf", C=1.0, epsilon=0.1)
    svr_model.fit(X_train_scaled, np.reshape(y_train_scaled, -1))
    svr_pred = svr_model.predict(feature_scaler.transform(X_test))
    svr_pred = target_scaler.inverse_transform(svr_pred.reshape(-1, 1)).flatten()

    # Print results for each split
    print("---------------- Linear Regression Model -----------------------------")
    print(f"RRSE: {root_relative_squared_error(y_test, lr_pred):.3f}")
    print(f"RAE: {relative_absolute_error(y_test, lr_pred):.3f}")
    print(f"RMSE: {np.sqrt(mean_squared_error(y_test, lr_pred)):.3f}")
    print(f"R² score: {r2_score(y_test, lr_pred):.3f}")
    print(f"MAE: {mean_absolute_error(y_test, lr_pred):.3f}")

    print("\n---------------- SVR Model -----------------------------")
    print(f"RRSE: {root_relative_squared_error(y_test, svr_pred):.3f}")
    print(f"RAE: {relative_absolute_error(y_test, svr_pred):.3f}")
    print(f"RMSE: {np.sqrt(mean_squared_error(y_test, svr_pred)):.3f}")
    print(f"R² score: {r2_score(y_test, svr_pred):.3f}")
    print(f"MAE: {mean_absolute_error(y_test, svr_pred):.3f}")
