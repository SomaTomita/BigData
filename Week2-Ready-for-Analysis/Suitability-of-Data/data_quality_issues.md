# Analysis of Data Quality Issues in Machine Learning

Based on Witten's Section 2.4 (Data Quality Issues: Missing Values, Inaccurate Values, and Unbalanced Data)

## ✅ Step 1: Three Types of Data Quality Issues and Examples

### 1. Missing Values

Values that are not measured or recorded.

**Examples:**

- Blood glucose level marked as "?" in medical data → due to equipment malfunction or doctor skipping measurement
- Income field left blank in customer surveys → respondent refused to answer

**Key Points:**

- Need to determine if missing data is "random" or "intentional (meaningful)"
- Typically represented as "?" or NaN
- While learning models often treat these as "simply unknown," the missing state itself can carry information

### 2. Inaccurate Values

Values that are present but clearly incorrect or meaningless.

**Examples:**

- Age recorded as "312 years" → input error (likely meant to be 31.2 years)
- "outlook" column containing "raini" → typo meant to be "rainy"

**Key Points:**

- Caused by data entry errors, type mismatches, abbreviation inconsistencies, or human errors
- Requires outlier detection for numerical values, dictionary checks or typo correction for nominal values
- If not corrected, models may learn non-existent categories

### 3. Unbalanced Data

Extreme disparity in class distribution (majority vs. minority).

**Examples:**

- Email classification data with "Spam: 5%, Non-spam: 95%"
- Medical diagnosis with "Disease: 2%, Healthy: 98%"

**Key Points:**

- Models can achieve seemingly high accuracy by simply predicting the majority class
- Accuracy alone can be misleading → need F1 score and AUC for better evaluation
- May require oversampling of minority class (e.g., SMOTE) for reinforcement

## ✅ Step 2: Which One is Different?

🔍 **Analysis:** Unbalanced Data stands out

Missing and inaccurate values → "Individual instances are broken"
Unbalanced data → "Overall distribution is skewed"

In other words:

- Missing / Inaccurate = local problems (row-level)
- Unbalanced = global problem (overall data distribution)

📌 **This difference is reflected in treatment methods:**

- Missing/incorrect values are handled through "removal or imputation"
- Imbalance is addressed through "class weight adjustment and sampling strategies"

## ✅ Step 3: Comparison Points (For Review)

- Do others consider "misrepresentation" or "intentional missing values (e.g., doctor's decision to skip tests)"?
- Are the examples realistic? (e.g., data errors likely to occur in banks or medical institutions)
- Have we explored deeper insights like "missing ≠ always random" or "imbalance = accuracy not trustworthy"?

## Summary

Missing values (like unmeasured blood glucose due to equipment failure), inaccurate values (like age=312 or outlook=raini), and unbalanced data (like spam:5%, non-spam:95%) represent different types of data quality issues. Notably, imbalance differs from the other two as it's not an instance-level error but a structural issue affecting the entire dataset, significantly impacting accuracy evaluation and algorithm selection.
