#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Confusion Matrix Analysis Script
This script demonstrates various evaluation techniques for classifiers using decision trees,
including percentage splits and cross-validation approaches.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    cohen_kappa_score,
)


class ConfusionMatrixAnalysis:
    def __init__(self, data_path):
        """
        Initialize the analysis with the dataset path.

        Args:
            data_path (str): Path to the weather nominal CSV file
        """
        self.weather_data = pd.read_csv(data_path)
        self.prepare_data()

    def prepare_data(self):
        """Prepare the data by separating features and target, and encoding categorical variables."""
        # Extract features and target
        self.features = self.weather_data.iloc[:, :4]
        self.output = self.weather_data.iloc[:, 4]

        # One-hot encode categorical features
        self.features_encoded = pd.get_dummies(self.features)

    def evaluate_full_dataset(self):
        """Evaluate the model on the entire training set."""
        print("\n=== Evaluation on Full Dataset ===")

        # Create and train decision tree
        dt = DecisionTreeClassifier(criterion="entropy", random_state=0)
        dt.fit(self.features_encoded, self.output)

        # Make predictions
        y_pred = dt.predict(self.features_encoded)

        # Calculate and display confusion matrix
        conf_matrix = confusion_matrix(self.output, y_pred)
        self._display_metrics(
            self.output, y_pred, dt.predict_proba(self.features_encoded)[:, 1]
        )

        return conf_matrix

    def evaluate_percentage_split(self, test_size):
        """
        Evaluate the model using a percentage split of the data.

        Args:
            test_size (float): Proportion of dataset to include in the test split
        """
        print(f"\n=== Evaluation with {int(test_size*100)}% Test Split ===")

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            self.features_encoded, self.output, test_size=test_size, random_state=42
        )

        # Create and train decision tree
        dt = DecisionTreeClassifier(criterion="entropy", random_state=0)
        dt.fit(X_train, y_train)

        # Make predictions
        y_pred = dt.predict(X_test)

        # Calculate and display metrics
        conf_matrix = confusion_matrix(y_test, y_pred)
        self._display_metrics(y_test, y_pred, dt.predict_proba(X_test)[:, 1])

        return conf_matrix

    def evaluate_cross_validation(self, n_folds):
        """
        Evaluate the model using k-fold cross-validation.

        Args:
            n_folds (int): Number of folds for cross-validation
        """
        print(f"\n=== Evaluation with {n_folds}-fold Cross-validation ===")

        # Initialize cross-validation
        cv = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=42)
        metrics = {
            "precision": [],
            "recall": [],
            "f1": [],
            "auc": [],
            "kappa": [],
            "fpr": [],
        }

        # Perform cross-validation
        for fold, (train_idx, test_idx) in enumerate(
            cv.split(self.features_encoded, self.output)
        ):
            print(f"\nFold {fold + 1}:")

            # Split data for this fold
            X_train = self.features_encoded.iloc[train_idx]
            X_test = self.features_encoded.iloc[test_idx]
            y_train = self.output.iloc[train_idx]
            y_test = self.output.iloc[test_idx]

            # Train and evaluate model
            dt = DecisionTreeClassifier(random_state=42)
            dt.fit(X_train, y_train)
            y_pred = dt.predict(X_test)
            y_prob = dt.predict_proba(X_test)[:, 1]

            # Calculate metrics for this fold
            fold_metrics = self._calculate_metrics(y_test, y_pred, y_prob)

            # Store metrics
            for metric, value in fold_metrics.items():
                metrics[metric].append(value)

            # Display confusion matrix for this fold
            conf_matrix = confusion_matrix(y_test, y_pred)
            print("\nConfusion Matrix:")
            print(conf_matrix)

        # Display average metrics across all folds
        print("\nAverage Metrics Across All Folds:")
        for metric, values in metrics.items():
            print(f"{metric.upper()}: {np.mean(values):.3f} (±{np.std(values):.3f})")

    def _calculate_metrics(self, y_true, y_pred, y_prob):
        """Calculate various performance metrics."""
        metrics = {}

        # Calculate basic metrics
        metrics["precision"] = precision_score(
            y_true, y_pred, pos_label="yes", zero_division=0
        )
        metrics["recall"] = recall_score(
            y_true, y_pred, pos_label="yes", zero_division=0
        )
        metrics["f1"] = f1_score(y_true, y_pred, pos_label="yes", zero_division=0)

        # Calculate ROC AUC if possible
        try:
            metrics["auc"] = roc_auc_score(y_true, y_prob)
        except ValueError:
            metrics["auc"] = np.nan

        # Calculate Kappa
        metrics["kappa"] = cohen_kappa_score(y_true, y_pred)

        # Calculate FPR
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        metrics["fpr"] = fp / (fp + tn) if (fp + tn) > 0 else 0

        return metrics

    def _display_metrics(self, y_true, y_pred, y_prob):
        """Display all calculated metrics."""
        metrics = self._calculate_metrics(y_true, y_pred, y_prob)

        print("\nPerformance Metrics:")
        print(f"Precision: {metrics['precision']:.3f}")
        print(f"Recall (TPR): {metrics['recall']:.3f}")
        print(f"F1 Score: {metrics['f1']:.3f}")
        print(f"False Positive Rate: {metrics['fpr']:.3f}")
        print(f"ROC AUC Score: {metrics['auc']:.3f}")
        print(f"Cohen's Kappa: {metrics['kappa']:.3f}")


def main():
    """Main function to run the analysis."""
    # Initialize analysis
    analysis = ConfusionMatrixAnalysis("weather.nominal.csv")

    # Evaluate on full dataset
    analysis.evaluate_full_dataset()

    # Evaluate with different percentage splits
    for split in [0.5, 0.6, 0.7]:
        analysis.evaluate_percentage_split(split)

    # Evaluate with different cross-validation folds
    for folds in [3, 4, 5]:
        analysis.evaluate_cross_validation(folds)


if __name__ == "__main__":
    main()
