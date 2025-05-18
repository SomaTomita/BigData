import pandas as pd
from sklearn.model_selection import train_test_split

# 1. Create sample categorical data
# This simulates a simple dataset about weather conditions and whether someone played outside
df = pd.DataFrame(
    {
        "Weather": ["Sunny", "Rainy", "Sunny", "Overcast", "Rainy", "Sunny"],
        "Play": ["Yes", "No", "Yes", "Yes", "No", "Yes"],
    }
)

# Display the original dataset
print("Original Dataset:")
print(df)
print("\n" + "=" * 50 + "\n")

# 2. Perform one-hot encoding on the 'Weather' column
# One-hot encoding converts categorical variables into a format that can be provided to ML algorithms
# Each unique category becomes a new column with binary values (0 or 1)
X = pd.get_dummies(df[["Weather"]])
y = df["Play"]

# Display the encoded features
print("Features after one-hot encoding:")
print(X)
print("\n" + "=" * 50 + "\n")

# 3. Split the data into training and testing sets
# We use a 70-30 split (70% training, 30% testing)
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,  # 30% of data will be used for testing
    random_state=42,  # Set for reproducibility
)

# Display the split results
print("Training Features (70% of data):")
print(X_train)
print("\nTraining Labels:")
print(y_train)
print("\nTesting Features (30% of data):")
print(X_test)
print("\nTesting Labels:")
print(y_test)

"""
Key Points:
-----------
1. pd.get_dummies():
   - Converts categorical variables into numerical format
   - Creates new binary columns for each category
   - Essential for machine learning models that require numerical input

2. train_test_split():
   - Splits data into training and testing sets
   - Helps evaluate model performance on unseen data
   - random_state ensures reproducibility
   - test_size determines the proportion of data used for testing

Usage:
------
Run this script to see how categorical data is preprocessed and split
for machine learning applications.
"""


# -------------------------------------------------------
# <Output>
# Original Dataset:
#     Weather Play
# 0     Sunny  Yes
# 1     Rainy   No
# 2     Sunny  Yes
# 3  Overcast  Yes
# 4     Rainy   No
# 5     Sunny  Yes

# ==================================================

# Features after one-hot encoding:
#    Weather_Overcast  Weather_Rainy  Weather_Sunny
# 0        False          False           True
# 1        False           True          False
# 2        False          False           True
# 3         True          False          False
# 4        False           True          False
# 5        False          False           True

# ==================================================

# Training Features (70% of data):
#    Weather_Overcast  Weather_Rainy  Weather_Sunny
# 5         False          False           True
# 2         False          False           True
# 4         False           True          False
# 3          True          False          False

# Training Labels:
# 5    Yes
# 2    Yes
# 4     No
# 3    Yes
# Name: Play, dtype: object

# Testing Features (30% of data):
#    Weather_Overcast  Weather_Rainy  Weather_Sunny
# 0        False          False           True
# 1        False           True          False

# Testing Labels:
# 0    Yes
# 1     No
# Name: Play, dtype: object
