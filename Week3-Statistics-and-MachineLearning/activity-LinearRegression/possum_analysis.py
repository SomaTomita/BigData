from math import log
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Load the data from CSV file
possum_data = pd.read_csv("possum.csv", delimiter=",", encoding="utf-8")

# Define independent and dependent variables
independent_variable = possum_data[["totalL"]]
dependent_variable = possum_data["headL"]
print(f"Independent Variable: {independent_variable}")
print(f"Dependent Variable: {dependent_variable}")

# Create and fit the linear regression model
model = LinearRegression()
model.fit(independent_variable, dependent_variable)

# Print model parameters
print(f"Intercept: {round(model.intercept_, 2)}")
print(f"Coefficient: {round(model.coef_[0], 2)}")

# Create test data for predictions
test = pd.DataFrame({"totalL": [70, 80, 85]})
print(f"Test: {test}")
predictions = model.predict(test)
print(f"Predictions: {predictions}")

# Print predictions
print("\nPredictions for total lengths [70, 80, 85]:")
# zip = Function to pair the elements of two iterables (array, list, etc.) one by one
# (70, 82.93) # loop 1
# (80, 88.59) # loop 2
# (85, 91.43) # loop 3
for length, pred in zip(test["totalL"], predictions):
    print(f"Total Length: {length} -> Predicted Head Length: {round(pred, 2)}")

# Create a scatter plot of the data with the regression line
plt.figure(figsize=(10, 6))
plt.scatter(
    independent_variable,
    dependent_variable,
    color="blue",
    alpha=0.5,
    label="Actual Data",
)
plt.plot(
    independent_variable,
    model.predict(independent_variable),
    color="red",
    label="Regression Line",
)
plt.xlabel("Total Length (cm)")
plt.ylabel("Head Length (mm)")
plt.title("Possum Head Length vs Total Length")
plt.legend()
plt.grid(True)
plt.savefig("possum_regression.png")
plt.close()

# Note about the units:
print("\nNote: There appears to be a unit mismatch in the data:")
print("- Head Length (headL) is measured in millimeters (mm)")
print("- Total Length (totalL) is measured in centimeters (cm)")
print("This explains why head length values appear larger than total length values.")


# -------------------------------------------------------
# <Output>
# Intercept: 43.26
# Coefficient: 0.57

# Predictions for total lengths [70, 80, 85]:
# Total Length: 70 -> Predicted Head Length: 82.93
# Total Length: 80 -> Predicted Head Length: 88.59
# Total Length: 85 -> Predicted Head Length: 91.43
