import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Read the dataset
df = pd.read_csv("../data/hotel-reservations.csv")

# Select relevant features for prediction
features = [
    "lead_time",
    "adr",
    "total_of_special_requests",
    "previous_cancellations",
    "previous_bookings_not_canceled",
]
X = df[features]
y = df["is_canceled"]

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Dictionary to store results
results = {}


# Function to evaluate model
def evaluate_model(model, X_train, X_test, y_train, y_test, model_name, split_ratio):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    return accuracy, report


# Different split ratios
split_ratios = [(0.8, 0.2), (0.7, 0.3), (0.6, 0.4)]

# Models to evaluate
models = {
    "Random Forest": RandomForestClassifier(random_state=42),
    "Logistic Regression": LogisticRegression(random_state=42, max_iter=1000),
}

# Evaluate models with different split ratios
for train_size, test_size in split_ratios:
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=test_size, random_state=42
    )

    for model_name, model in models.items():
        accuracy, report = evaluate_model(
            model,
            X_train,
            X_test,
            y_train,
            y_test,
            model_name,
            f"{int(train_size*100)}/{int(test_size*100)}",
        )

        key = f"{model_name}_{int(train_size*100)}_{int(test_size*100)}"
        results[key] = {"accuracy": accuracy, "report": report}

# Create visualization for accuracy comparison
plt.figure(figsize=(12, 6))
split_labels = ["80/20", "70/30", "60/40"]
rf_accuracies = [
    results[f"Random Forest_{int(split[0]*100)}_{int(split[1]*100)}"]["accuracy"]
    for split in split_ratios
]
lr_accuracies = [
    results[f"Logistic Regression_{int(split[0]*100)}_{int(split[1]*100)}"]["accuracy"]
    for split in split_ratios
]

x = np.arange(len(split_labels))
width = 0.35

plt.bar(x - width / 2, rf_accuracies, width, label="Random Forest")
plt.bar(x + width / 2, lr_accuracies, width, label="Logistic Regression")

plt.xlabel("Train/Test Split Ratio")
plt.ylabel("Accuracy")
plt.title("Model Performance Comparison")
plt.xticks(x, split_labels)
plt.legend()

plt.tight_layout()
plt.savefig("model_comparison.png")
plt.close()

# Print results
for key, value in results.items():
    print(f"\n{key} Results:")
    print(f"Accuracy: {value['accuracy']:.4f}")
    print("Classification Report:")
    print(value["report"])
