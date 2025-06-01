import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv("weather.nominal.csv")

# Remove whitespace from column names
data.columns = [col.strip() for col in data.columns]

# Convert categorical variables to numerical values
le = LabelEncoder()
for column in data.columns:
    if data[column].dtype == "object":
        data[column] = le.fit_transform(data[column])

# Split features and target variable
X = data.drop("play", axis=1)
y = data["play"]

# Initialize models
dt_classifier = DecisionTreeClassifier(random_state=42)
nb_classifier = GaussianNB()
svm_classifier = SVC(kernel="linear", random_state=42)

# Dictionary to store evaluation results
results = {}


# 1. Full training set evaluation
def evaluate_full_training(classifier, name):
    classifier.fit(X, y)
    y_pred = classifier.predict(X)
    return classification_report(y, y_pred, output_dict=True)


# 2. 7-fold cross-validation
def evaluate_cross_validation(classifier):
    scores = cross_val_score(classifier, X, y, cv=7)
    return scores.mean()


# 3. 50% split evaluation
def evaluate_split(classifier, name):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.5, random_state=42
    )
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    return classification_report(y_test, y_pred, output_dict=True)


# Evaluate each model
classifiers = {
    "Decision Tree": dt_classifier,
    "Naive Bayes": nb_classifier,
    "SVM": svm_classifier,
}

for name, classifier in classifiers.items():
    results[name] = {
        "full_training": evaluate_full_training(classifier, name),
        "cross_validation": evaluate_cross_validation(classifier),
        "split_50": evaluate_split(classifier, name),
    }

# Visualize results
plt.figure(figsize=(15, 5))

# Compare accuracy across evaluation methods
methods = ["full_training", "cross_validation", "split_50"]
x = np.arange(len(classifiers))
width = 0.25

for i, method in enumerate(methods):
    accuracies = []
    for name in classifiers.keys():
        if method == "cross_validation":
            accuracies.append(results[name][method])
        else:
            accuracies.append(results[name][method]["accuracy"])

    plt.bar(x + i * width, accuracies, width, label=method)

plt.xlabel("Classifiers")
plt.ylabel("Accuracy")
plt.title("Classifier Performance Comparison")
plt.xticks(x + width, classifiers.keys())
plt.legend()
plt.tight_layout()
plt.savefig("classifier_comparison.png")
plt.close()

# Generate markdown report
markdown_content = """# Weather Data Classification Analysis Report

## 1. Overview
This report compares the performance of three different classifiers (Decision Tree, Naive Bayes, and SVM)
on the weather dataset using three evaluation methods (full training set, 7-fold cross-validation, and 50% split).

## 2. Dataset Information
- Dataset: weather.nominal.csv
- Features: outlook, temperature, humidity, windy
- Target variable: play
- Number of instances: {len(data)}

## 3. Evaluation Results

### 3.1 Full Training Set Evaluation
"""

for name in classifiers.keys():
    markdown_content += f"\n#### {name}\n"
    markdown_content += (
        f"- Accuracy: {results[name]['full_training']['accuracy']:.3f}\n"
    )
    markdown_content += f"- Detailed Performance Metrics:\n"
    markdown_content += "```\n"
    markdown_content += f"{pd.DataFrame(results[name]['full_training']).to_string()}\n"
    markdown_content += "```\n"

markdown_content += "\n### 3.2 7-Fold Cross-Validation Results\n"
for name in classifiers.keys():
    markdown_content += f"- {name}: {results[name]['cross_validation']:.3f}\n"

markdown_content += "\n### 3.3 50% Split Evaluation Results\n"
for name in classifiers.keys():
    markdown_content += f"\n#### {name}\n"
    markdown_content += f"- Accuracy: {results[name]['split_50']['accuracy']:.3f}\n"
    markdown_content += f"- Detailed Performance Metrics:\n"
    markdown_content += "```\n"
    markdown_content += f"{pd.DataFrame(results[name]['split_50']).to_string()}\n"
    markdown_content += "```\n"

markdown_content += """
## 4. Conclusions
The comparison of classifier performance yields the following insights:

1. While all classifiers show relatively high accuracy on the full training set, this may indicate potential overfitting.

2. 7-fold cross-validation provides a more realistic performance assessment, revealing clearer differences between classifiers.

3. The 50% split evaluation helps assess generalization capability and predict real-world performance.

## 5. Visualization
A comparative visualization of classifier performance has been saved as `classifier_comparison.png`.
This graph allows comparison of accuracy across different evaluation methods for each classifier.
"""

with open("weather_analysis_report.md", "w") as f:
    f.write(markdown_content)
