import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


def load_and_prepare_data():
    """
    Load the weather data and prepare it for the decision tree classifier.
    Returns:
        tuple: (features_encoded, output) - preprocessed features and target variable
    """
    # Load the data from CSV file
    weather_data = pd.read_csv("weather.nominal.csv", delimiter=",", encoding="utf-8")

    # Select features (all columns except the last one)
    features = weather_data.iloc[:, :4]
    output = weather_data.iloc[:, 4]

    # Encode categorical features using one-hot encoding
    print(f"Features: {features}")
    features_encoded = pd.get_dummies(features)
    print(f"Features Encoded: {features_encoded}")

    return features_encoded, output


def create_and_train_model(features_encoded, output, test_size=0.4):
    """
    Create and train the decision tree model.
    Args:
        features_encoded: Preprocessed feature data
        output: Target variable
        test_size: Proportion of dataset to include in the test split
    Returns:
        tuple: (model, features_train, features_test, output_train, output_test)
    """
    # Split the dataset into training and testing sets
    features_train, features_test, output_train, output_test = train_test_split(
        features_encoded, output, random_state=0, test_size=test_size
    )

    # Create the decision tree classifier
    decision_tree = DecisionTreeClassifier(
        criterion="entropy", splitter="best", random_state=0
    )

    # Train the model
    decision_tree.fit(features_train, output_train)

    return decision_tree, features_train, features_test, output_train, output_test


def visualize_tree(decision_tree, feature_names):
    """
    Visualize the decision tree.
    Args:
        decision_tree: Trained decision tree model
        feature_names: Names of the features
    """
    plt.figure(figsize=(12, 6))
    plot_tree(
        decision_tree,
        feature_names=feature_names,
        class_names=decision_tree.classes_,
        filled=True,
    )
    plt.savefig("decision_tree.png")
    plt.close()


def main():
    # Load and prepare the data
    features_encoded, output = load_and_prepare_data()

    # Create and train the model
    decision_tree, features_train, features_test, output_train, output_test = (
        create_and_train_model(features_encoded, output)
    )

    # Visualize the decision tree
    visualize_tree(decision_tree, features_encoded.columns)

    # Print model accuracy
    train_score = decision_tree.score(features_train, output_train)
    test_score = decision_tree.score(features_test, output_test)

    print(f"Training Accuracy: {train_score:.2f}")
    print(f"Testing Accuracy: {test_score:.2f}")


if __name__ == "__main__":
    main()


# -------------------------------------------------------
# <Output>
# Features: outlook  temperature  humidity  windy
# 0          sunny         hot      high   False
# 1          sunny         hot      high    True
# 2       overcast         hot      high   False
# 3          rainy        mild      high   False
# 4          rainy        cool    normal   False
# 5          rainy        cool    normal    True
# 6       overcast        cool    normal    True
# 7          sunny        mild      high   False
# 8          sunny        cool    normal   False
# 9          rainy        mild    normal   False
# 10         sunny        mild    normal    True
# 11      overcast        mild      high    True
# 12      overcast         hot    normal   False
# 13         rainy        mild      high    True

# Features Encoded:    windy  outlook_overcast  outlook_rainy     outlook_sunny  temperature_cool  temperature_hot  temperature_mild  humidity_high  humidity_normal
# 0                  False             False          False           True              False              True              False            True             False
# 1                   True             False          False           True              False              True              False            True             False
# 2                  False              True          False          False              False              True              False            True             False
# 3                  False             False           True          False              False             False               True            True             False
# 4                  False             False           True          False               True             False              False           False              True
# 5                   True             False           True          False               True             False              False           False              True
# 6                   True              True          False          False               True             False              False           False              True
# 7                  False             False          False           True              False             False               True            True             False
# 8                  False             False          False           True               True             False              False           False              True
# 9                  False             False           True          False              False             False               True           False              True
# 10                  True             False          False           True              False             False               True           False              True
# 11                  True              True          False          False              False             False               True            True             False
# 12                 False              True          False          False              False              True              False           False              True
# 13                  True             False           True          False              False             False               True            True             False

# Training Accuracy: 1.00
# Testing Accuracy: 0.33
