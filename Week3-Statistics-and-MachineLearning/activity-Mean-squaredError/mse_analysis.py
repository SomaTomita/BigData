"""
Linear Regression Analysis using Mean-Squared Error (MSE)
This script performs linear regression analysis on possum data using both percentage split
and cross-validation approaches to evaluate model performance.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Part 1: Percentage Split Analysis
print("=" * 80)
print("PART 1: PERCENTAGE SPLIT ANALYSIS")
print("=" * 80)

# Load the possum dataset
possum_data = pd.read_csv(
    "../activity-LinearRegression/possum.csv", delimiter=",", encoding="utf-8"
)

# Define independent (totalL) and dependent (headL) variables
independent_variable = possum_data[["totalL"]]
dependent_variable = possum_data["headL"]

# Create the linear regression model
model = LinearRegression()

# Dictionary to store results for summary table
percentage_split_results = []

# Perform analysis with different train-test splits (80%, 70%, 60%, 50%)
for split in [0.8, 0.7, 0.6, 0.5]:
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        independent_variable,
        dependent_variable,
        test_size=split,
        random_state=42,  # For reproducibility
    )

    # Fit the model on training data
    model.fit(X_train, y_train)

    # Make predictions on test data
    y_pred = model.predict(X_test)

    # Calculate performance metrics
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Store results
    percentage_split_results.append(
        {
            "split": split,
            "train_size": 1 - split,
            "mse": mse,
            "mae": mae,
            "r2": r2,
            "intercept": model.intercept_,
            "coefficient": model.coef_[0],
        }
    )

    # Print results
    print("-" * 65)
    print(f"For a split of {round((1-split)*100)}% training / {round(split*100)}% test")
    print(
        f"Model equation: y = {round(model.intercept_,2)} + {round(model.coef_[0],2)} x"
    )
    print(f"Mean Squared Error (MSE): {mse:.3f}")
    print(f"Mean Absolute Error (MAE): {mae:.3f}")
    print(f"R² Score: {r2:.3f}")
    print("-" * 65)

# Part 2: Cross-Validation Analysis
print("\n")
print("=" * 80)
print("PART 2: CROSS-VALIDATION ANALYSIS")
print("=" * 80)

# Dictionary to store cross-validation results
cv_results = []

# Perform cross-validation with different numbers of folds
for folds in [10, 20, 30, 40]:
    # Define scoring metrics for cross-validation
    scoring = ["neg_mean_absolute_error", "neg_mean_squared_error", "r2"]

    # Perform cross-validation
    results = cross_validate(
        model,
        independent_variable,
        dependent_variable,
        cv=folds,
        scoring=scoring,
        return_estimator=True,
    )

    # Calculate average metrics across all folds
    avg_mse = -np.mean(results["test_neg_mean_squared_error"])
    avg_mae = -np.mean(results["test_neg_mean_absolute_error"])
    avg_r2 = np.mean(results["test_r2"])

    # Store results
    cv_results.append(
        {"folds": folds, "avg_mse": avg_mse, "avg_mae": avg_mae, "avg_r2": avg_r2}
    )

    # Print results for each fold
    print(f"\nResults for {folds}-fold Cross-Validation:")
    print("-" * 65)
    for i in range(folds):
        print(f"Fold {i+1}:")
        print(
            f"Model equation: y = {results['estimator'][i].coef_[0]:.2f} x + {results['estimator'][i].intercept_:.2f}"
        )
        print(f"MSE: {-results['test_neg_mean_squared_error'][i]:.3f}")
        print(f"MAE: {-results['test_neg_mean_absolute_error'][i]:.3f}")
        print(f"R²: {results['test_r2'][i]:.3f}")
        print("-" * 65)

    # Print average metrics
    print(f"\nAverage metrics for {folds}-fold Cross-Validation:")
    print(f"Average MSE: {avg_mse:.3f}")
    print(f"Average MAE: {avg_mae:.3f}")
    print(f"Average R²: {avg_r2:.3f}")
    print("=" * 65)

# Create and display summary tables
print("\nSummary Tables:")
print("\n1. Percentage Split Results:")
print("-" * 80)
print("Train/Test Split | MSE    | MAE    | R²     | Model Equation")
print("-" * 80)
for result in percentage_split_results:
    print(
        f"{result['train_size']*100:2.0f}/{result['split']*100:2.0f}         | {result['mse']:.3f} | {result['mae']:.3f} | {result['r2']:.3f} | y = {result['intercept']:.2f} + {result['coefficient']:.2f}x"
    )

print("\n2. Cross-Validation Results:")
print("-" * 80)
print("Folds | Avg MSE | Avg MAE | Avg R²")
print("-" * 80)
for result in cv_results:
    print(
        f"{result['folds']:5d} | {result['avg_mse']:.3f}  | {result['avg_mae']:.3f}  | {result['avg_r2']:.3f}"
    )

"""
Analysis Notes:
1. Percentage Split Analysis:
   - Shows how model performance varies with different training/test splits
   - Generally, larger training sets (smaller test splits) tend to give better results
   - MSE and MAE provide absolute error measures in the original units
   - R² indicates the proportion of variance explained by the model

2. Cross-Validation Analysis:
   - More robust evaluation as each data point is used for both training and testing
   - Higher number of folds generally gives more stable results
   - Helps identify if the model is stable across different data subsets
   - Average metrics provide a more reliable estimate of model performance

Available Metrics in sklearn:
1. Regression metrics:
   - neg_mean_squared_error (MSE)
   - neg_mean_absolute_error (MAE)
   - r2 (R-squared)
   - neg_root_mean_squared_error (RMSE)
   - neg_median_absolute_error
   - explained_variance
   - max_error

2. Additional considerations:
   - RMSE (Root Mean Squared Error) is often preferred as it's in the same units as the target variable
   - MAE is more robust to outliers than MSE
   - R² should be used alongside other metrics as it can be misleading in some cases
"""

"""
Comprehensive Discussion on Error Metrics and Machine Learning Insights:

1. Choosing Appropriate Error Metrics:
   - The choice of error metrics depends heavily on the specific application context
   - There is no "one-size-fits-all" metric for all machine learning problems
   - The selection should be based on domain knowledge and business requirements

2. Characteristics of Different Error Metrics:
   a) Squared Error Metrics (MSE):
      - Penalizes larger errors more heavily than smaller ones
      - Useful when large errors are particularly undesirable
      - Can be sensitive to outliers
      - Units are squared (different from original measurements)

   b) Root Mean Squared Error (RMSE):
      - Similar to MSE but maintains the same units as the original data
      - Makes interpretation more intuitive
      - Still penalizes larger errors more heavily
      - Commonly used in practice due to its interpretability

   c) Mean Absolute Error (MAE):
      - Treats all errors linearly (no extra penalty for larger errors)
      - More robust to outliers than MSE/RMSE
      - Easier to interpret but may not capture critical large errors
      - Preferred when outliers should not have overwhelming influence

   d) Relative Error Metrics (R²):
      - Accounts for the inherent predictability of the target variable
      - Compensates for variables that naturally cluster around their mean
      - Helps compare models across different scales and domains
      - Should be used alongside absolute metrics for complete evaluation

3. Contextual Considerations:
   - Large errors in some contexts may be more critical than in others
   - The scale of the target variable affects the interpretation of absolute metrics
   - Domain-specific requirements should guide metric selection
   - Consider using multiple metrics for a more complete evaluation

4. Evolution of "Good Machine Learning" Definition:
   Based on these exercises and analyses, a refined definition of good machine learning might include:
   - Appropriate metric selection based on context
   - Robust validation strategies (cross-validation, proper train-test splits)
   - Understanding of model limitations and assumptions
   - Balance between model complexity and interpretability
   - Consideration of both statistical and practical significance
   - Recognition that "good" is context-dependent and not just about numbers

5. Key Learnings:
   - Error metrics are tools for understanding model performance, not absolute truths
   - The choice of metric can significantly influence model selection and optimization
   - Cross-validation provides more robust performance estimates than single splits
   - Larger training sets generally lead to better performance, but with diminishing returns
   - The relationship between different error metrics provides insights into model behavior
   - A holistic approach to model evaluation is more valuable than focusing on a single metric

6. Practical Recommendations:
   - Always use multiple error metrics for evaluation
   - Consider the business impact of different types of errors
   - Document the rationale for choosing specific metrics
   - Regularly revisit and validate metric choices as requirements evolve
   - Use cross-validation when possible, especially with limited data
   - Consider the interpretability of metrics when communicating results

This analysis demonstrates that machine learning is not just about achieving the lowest error numbers, but about understanding the context, choosing appropriate evaluation methods, and making informed decisions based on multiple factors. The definition of "good machine learning" has evolved to emphasize the importance of this holistic approach over simple metric optimization.
"""
