# Alternative Forms of Regression Analysis

## Problem Description

When working with the "possum.arff" data in WEKA, you may notice that functions under the classify tab such as SimpleLinearRegression and LinearRegression are not available for selection, and while SMOreg is available, it won't work. This is due to the presence of String attributes ("pop" and "sex") in the "possum.arff" file, which WEKA cannot handle directly. Additionally, some functions are designed to work only with numeric data (e.g., SimpleLinearRegression).

## Solution Approach

To address this issue, we implement the following steps:

1. Data Preprocessing

   - Converting string data to numeric format
   - Applying one-hot encoding for categorical variables
   - Feature scaling (especially important for SVR)

2. Implementation of Multiple Regression Methods

   - Linear Regression
   - Support Vector Regression (SVR)

3. Performance Evaluation
   - Using various metrics (RMSE, MAE, R², RRSE, RAE)
   - Comparing results across different test/train splits

## Implementation Details

### Data Preparation

```python
# Convert categorical variables
possum_encoded = pd.get_dummies(possum_data)

# Select features and target
features_data = possum_encoded[['site', 'age', 'headL', 'skullW ', 'totalL', 'sex_m', 'sex_f']]
target_data = possum_encoded['tailL']
```

### Model Training and Evaluation

- Full dataset evaluation
- Percentage split evaluation (20%, 30%, 40%, 50%)
- Cross-validation analysis

## Experimental Results and Analysis

### Full Dataset Results

#### Linear Regression Performance

- RRSE: 0.583 (58.3% relative error)
- RAE: 0.553 (55.3% absolute error)
- RMSE: 1.138 units
- R² score: 0.661 (66.1% variance explained)
- MAE: 0.867 units

#### SVR Performance

- RRSE: 0.524 (52.4% relative error)
- RAE: 0.456 (45.6% absolute error)
- RMSE: 1.023 units
- R² score: 0.726 (72.6% variance explained)
- MAE: 0.715 units

**Key Findings:**

1. SVR outperforms Linear Regression across all metrics
2. SVR explains 72.6% of variance compared to 66.1% for Linear Regression
3. SVR shows lower error rates in both absolute and relative terms

### Percentage Split Analysis

#### 20% Test Split

- SVR shows better performance (R² = 0.409) compared to Linear Regression (R² = 0.167)
- Both models show degraded performance compared to full dataset
- Error metrics increase but SVR maintains better performance

#### 30% Test Split

- SVR maintains better performance (R² = 0.481)
- Linear Regression shows significant degradation (R² = 0.092)
- Error metrics continue to favor SVR

#### 40% Test Split

- Similar pattern continues with SVR performing better
- Linear Regression shows slight improvement from 30% split
- SVR maintains more consistent performance

#### 50% Test Split

- Both models show some performance degradation
- SVR continues to outperform Linear Regression
- Larger test set shows impact on model stability

### Performance Trends

1. **Model Stability**

   - SVR shows more consistent performance across different splits
   - Linear Regression performance varies more significantly
   - Both models perform best with more training data

2. **Error Patterns**

   - SVR consistently maintains lower error rates
   - RMSE and MAE increase with larger test splits
   - Relative errors (RRSE, RAE) show similar patterns

3. **Model Comparison**
   - SVR is consistently superior across all metrics
   - Performance gap is largest with full dataset
   - Both models show sensitivity to train/test split ratio

## Conclusions

1. **Model Selection**

   - SVR is the recommended choice for this dataset
   - Shows better performance and stability
   - More robust across different data splits

2. **Training Considerations**

   - Larger training sets produce better results
   - 70-30 or 80-20 splits appear optimal
   - Cross-validation important for robust evaluation

3. **Practical Implications**
   - SVR's superior performance justifies additional computational cost
   - Feature scaling is crucial for optimal results
   - Regular retraining with new data recommended

## Notes

- Cross-validation helps provide more robust performance estimates
- Feature scaling is particularly important for SVR
- Model selection should be based on both performance metrics and problem requirements
