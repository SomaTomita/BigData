# Multiple Linear Regression

## Overview

Multiple Linear Regression (MLR) is a statistical technique used to model the relationship between one dependent variable (target variable) and two or more independent variables (predictor variables). It extends simple linear regression to understand more complex data relationships.

## Basic Equation

The fundamental equation for multiple linear regression is:

```
y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ + ε

where:
- y: Dependent variable (prediction target)
- β₀: Intercept
- βᵢ: Coefficients for each independent variable
- xᵢ: Independent variables
- ε: Error term
```

### Example:

```
House Price = β₀ + β₁(Square Footage) + β₂(Number of Bedrooms) + β₃(Age of House) + ε

Concrete values:
Price = 100,000 + 150(2000 sq ft) + 15000(3 bedrooms) - 1000(20 years)
     = 100,000 + 300,000 + 45,000 - 20,000
     = $425,000
```

## Key Assumptions

| Assumption       | Description                                                            | Impact if Violated               |
| ---------------- | ---------------------------------------------------------------------- | -------------------------------- |
| Linearity        | Linear relationship exists between independent and dependent variables | Decreased prediction accuracy    |
| Independence     | No strong correlation between independent variables                    | Multicollinearity issues         |
| Homoscedasticity | Constant variance in errors                                            | Inefficient estimates            |
| Normality        | Residuals follow normal distribution                                   | Inaccurate statistical inference |

## Data Preprocessing Steps

1. **Normalization**

   - Min-Max Scaling:
     ```python
     x_normalized = (x - min(x)) / (max(x) - min(x))
     # Example: Age [20, 40, 60] → [0, 0.5, 1]
     ```
   - Z-score Standardization:
     ```python
     z_score = (x - mean(x)) / std(x)
     # Example: Heights [160, 170, 180] → [-1, 0, 1]
     ```

2. **Missing Value Treatment**

   - Mean/Median Imputation
   - Record Deletion
   - Advanced Imputation Methods

   Example:

   ```python
   # Original data: [10, 15, nan, 20, 25]
   # Mean imputation: [10, 15, 17.5, 20, 25]
   ```

3. **Outlier Treatment**

   - Removal
   - Capping
   - Log Transformation

   Example:

   ```python
   # Original: [100, 120, 115, 500, 110]
   # After capping at 95th percentile: [100, 120, 115, 150, 110]
   ```

4. **Categorical Variable Processing**

   ```
   Example: Color (red, blue, green)

   Original → One-Hot Encoded
   red      → [1, 0, 0]
   blue     → [0, 1, 0]
   green    → [0, 0, 1]

   Example: Education Level (ordinal)
   high school → 1
   bachelor    → 2
   master      → 3
   doctorate   → 4
   ```

## Model Evaluation Metrics

| Metric                            | Description                                                    | Optimal Value |
| --------------------------------- | -------------------------------------------------------------- | ------------- |
| R² (Coefficient of Determination) | Proportion of variance explained by model                      | Closer to 1   |
| Residual Sum of Squares (RSS)     | Sum of squared differences between actual and predicted values | Closer to 0   |
| Mean Squared Error (MSE)          | Average magnitude of prediction errors                         | Closer to 0   |
| Adjusted R²                       | R² adjusted for number of variables                            | Closer to 1   |

### Example Interpretation:

```
R² = 0.85 means the model explains 85% of the variance in the target variable
MSE = 100 means the average squared prediction error is 100 units
```

## Handling Multicollinearity

1. **Variable Selection**

   - Forward Selection
   - Backward Elimination
   - Stepwise Selection

   Example:

   ```
   Starting with: [x₁, x₂, x₃, x₄, x₅]
   Step 1: Select x₃ (highest correlation with y)
   Step 2: Add x₁ (next best predictor)
   Final model: y = β₀ + β₁x₁ + β₃x₃
   ```

2. **Regularization Techniques**
   - Ridge Regression (L2)
   - Lasso Regression (L1)
   - Elastic Net (L1+L2)

## Practical Tips

- Dedicate sufficient time to preprocessing as data quality significantly impacts results
- Consider both theoretical basis and statistical criteria for variable selection
- Use cross-validation to evaluate model generalization
- Leverage domain expertise for result interpretation

### Example Cross-Validation:

```python
# 5-fold cross-validation
Train: [Fold 1,2,3,4] Test: [Fold 5]
Train: [Fold 1,2,3,5] Test: [Fold 4]
Train: [Fold 1,2,4,5] Test: [Fold 3]
Train: [Fold 1,3,4,5] Test: [Fold 2]
Train: [Fold 2,3,4,5] Test: [Fold 1]
```

## Limitations and Alternatives

### Limitations

- Difficulty in expressing non-linear relationships
- Sensitivity to outliers
- Multicollinearity issues
- Underfitting in high-dimensional data

### Alternative Methods

1. Polynomial Regression
   ```
   y = β₀ + β₁x + β₂x² + β₃x³
   ```
2. Decision Trees
3. Neural Networks
4. Other Machine Learning Methods

### Example of When to Use Alternatives:

```
Scenario: House Price Prediction
- Linear relationship: Use MLR
  Price = β₀ + β₁(size) + β₂(bedrooms)

- Non-linear relationship: Use Polynomial
  Price = β₀ + β₁(size) + β₂(size²)

- Complex patterns: Use Neural Network
  When multiple non-linear interactions exist
```

## Summary

Multiple Linear Regression serves as a baseline model in many practical applications due to its interpretability and ease of implementation. However, understanding its assumptions and limitations is crucial, as is proper preprocessing and model evaluation. For complex patterns, consider using more advanced techniques.
