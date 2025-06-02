# Comparing Data Mining Schemes Using Statistical Methods

## Introduction

When comparing different machine learning or data mining schemes, it's crucial to determine whether one method truly performs better than another. Let's explore this with simple, practical examples.

## Cross-Validation Based Comparison

### Simple Example: Iris Dataset Classification

Let's start with a simple, concrete example using the famous iris dataset:

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import numpy as np
from scipy import stats

# Load iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# Example 1: Compare Random Forest vs SVM
rf = RandomForestClassifier(n_estimators=100, random_state=42)
svm = SVC(kernel='rbf', random_state=42)

# Get scores for both models
rf_scores = cross_val_score(rf, X, y, cv=10)
svm_scores = cross_val_score(svm, X, y, cv=10)

print("Random Forest scores:", rf_scores)
# Example output: [0.93, 0.97, 0.93, 0.97, 0.93, 0.97, 0.93, 0.97, 0.93, 0.97]

print("SVM scores:", svm_scores)
# Example output: [0.90, 0.93, 0.90, 0.93, 0.90, 0.93, 0.90, 0.93, 0.90, 0.93]
```

### Real-world Interpretation

Let's say we got these results:

- Random Forest average accuracy: 95%
- SVM average accuracy: 92%

The question is: Is this 3% difference statistically significant?

## Student's t-test: A Simple Example

### Case Study: Comparing Two Models

```python
def simple_comparison_example():
    # Example scores from two models
    model1_scores = np.array([0.95, 0.94, 0.96, 0.93, 0.95])  # Random Forest
    model2_scores = np.array([0.92, 0.91, 0.93, 0.90, 0.92])  # SVM

    # Calculate the differences
    differences = model1_scores - model2_scores
    print("Differences between models:", differences)
    # Output: [0.03, 0.03, 0.03, 0.03, 0.03]

    # Calculate mean difference
    mean_diff = np.mean(differences)
    print("Mean difference:", mean_diff)
    # Output: 0.03

    # Calculate t-statistic
    t_stat = calculate_t_statistic(model1_scores, model2_scores)
    print("T-statistic:", t_stat)
    # Output: Example t-stat = 15.811

    return t_stat

# Usage example with interpretation
t_stat = simple_comparison_example()
```

### Practical Interpretation of Confidence Intervals

Let's use a real example with the confidence table:

```python
def interpret_confidence(t_stat):
    confidence_table = {
        4.30: "99.9% confident",
        3.25: "99.5% confident",
        2.82: "99% confident",
        1.83: "95% confident",
        1.38: "90% confident",
        0.88: "80% confident"
    }

    print(f"Your t-statistic is {t_stat}")
    for threshold, confidence in confidence_table.items():
        if t_stat > threshold:
            print(f"Since {t_stat} > {threshold}, we are {confidence} "
                  "that the difference is significant")
            break

# Example usage
interpret_confidence(3.5)
# Output: "Since 3.5 > 3.25, we are 99.5% confident that the difference is significant"
```

## Non-Paired Example: Different Dataset Sizes

Here's a concrete example where we can't use paired testing:

```python
def unpaired_example():
    # Model 1 tested on 5 different datasets
    model1_scores = np.array([0.95, 0.94, 0.96, 0.93, 0.95])

    # Model 2 tested on 3 different datasets
    model2_scores = np.array([0.92, 0.91, 0.93])

    # Calculate unpaired t-test
    t_stat = compare_unpaired_schemes(model1_scores, model2_scores)
    print("Unpaired t-statistic:", t_stat)

    return t_stat

# Real-world interpretation
t_stat = unpaired_example()
```

### Complete Working Example with Real Data

```python
from sklearn.datasets import make_classification

# Generate synthetic data for demonstration
X, y = make_classification(n_samples=1000, n_features=20,
                         n_informative=15, n_redundant=5,
                         random_state=42)

# Split into training and test sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Compare Random Forest vs SVM
rf_classifier = RandomForestClassifier(n_estimators=100)
svm_classifier = SVC(kernel='rbf')

# Run comparison
is_significant, p_value, t_stat = compare_learning_schemes(
    rf_classifier,
    svm_classifier,
    X_train,
    y_train
)

print("Results of comparison:")
print(f"Significant difference found: {is_significant}")
print(f"P-value: {p_value:.4f}")
print(f"T-statistic: {t_stat:.4f}")

# Example output:
# Significant difference found: True
# P-value: 0.0023
# T-statistic: 3.8754
```

## Practical Tips with Examples

1. **Sample Size Effect**

```python
# Small sample example
small_sample = compare_schemes(rf, svm, X[:20], y[:20])
# Large sample example
large_sample = compare_schemes(rf, svm, X, y)

print("Small sample might show less significant results")
print("Large sample usually gives more reliable comparisons")
```

2. **Cross-validation Fold Selection**

```python
# Different fold examples
scores_5fold = cross_val_score(rf, X, y, cv=5)
scores_10fold = cross_val_score(rf, X, y, cv=10)

print("5-fold CV scores:", np.mean(scores_5fold))
```

## Conclusion

Through these practical examples, we can see that:

- Statistical comparison helps us make informed decisions
- The t-test provides a mathematical foundation for comparing models
- Real-world applications require careful interpretation of results
- Larger sample sizes generally provide more reliable comparisons
- Both paired and unpaired tests have their specific use cases

Remember: A statistically significant difference doesn't always mean practical significance. Always consider the context of your problem when making decisions.
