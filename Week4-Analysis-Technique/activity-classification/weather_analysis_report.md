# Weather Data Classification Analysis Report

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

#### Decision Tree
- Accuracy: 1.000
- Detailed Performance Metrics:
```
             0    1  accuracy  macro avg  weighted avg
precision  1.0  1.0       1.0        1.0           1.0
recall     1.0  1.0       1.0        1.0           1.0
f1-score   1.0  1.0       1.0        1.0           1.0
support    5.0  9.0       1.0       14.0          14.0
```

#### Naive Bayes
- Accuracy: 0.929
- Detailed Performance Metrics:
```
                  0         1  accuracy  macro avg  weighted avg
precision  1.000000  0.900000  0.928571   0.950000      0.935714
recall     0.800000  1.000000  0.928571   0.900000      0.928571
f1-score   0.888889  0.947368  0.928571   0.918129      0.926483
support    5.000000  9.000000  0.928571  14.000000     14.000000
```

#### SVM
- Accuracy: 0.857
- Detailed Performance Metrics:
```
              0         1  accuracy  macro avg  weighted avg
precision  1.00  0.818182  0.857143   0.909091      0.883117
recall     0.60  1.000000  0.857143   0.800000      0.857143
f1-score   0.75  0.900000  0.857143   0.825000      0.846429
support    5.00  9.000000  0.857143  14.000000     14.000000
```

### 3.2 7-Fold Cross-Validation Results
- Decision Tree: 0.571
- Naive Bayes: 0.571
- SVM: 0.643

### 3.3 50% Split Evaluation Results

#### Decision Tree
- Accuracy: 0.714
- Detailed Performance Metrics:
```
             0    1  accuracy  macro avg  weighted avg
precision  0.5  0.8  0.714286       0.65      0.714286
recall     0.5  0.8  0.714286       0.65      0.714286
f1-score   0.5  0.8  0.714286       0.65      0.714286
support    2.0  5.0  0.714286       7.00      7.000000
```

#### Naive Bayes
- Accuracy: 0.571
- Detailed Performance Metrics:
```
                  0         1  accuracy  macro avg  weighted avg
precision  0.333333  0.750000  0.571429   0.541667      0.630952
recall     0.500000  0.600000  0.571429   0.550000      0.571429
f1-score   0.400000  0.666667  0.571429   0.533333      0.590476
support    2.000000  5.000000  0.571429   7.000000      7.000000
```

#### SVM
- Accuracy: 0.571
- Detailed Performance Metrics:
```
                  0         1  accuracy  macro avg  weighted avg
precision  0.333333  0.750000  0.571429   0.541667      0.630952
recall     0.500000  0.600000  0.571429   0.550000      0.571429
f1-score   0.400000  0.666667  0.571429   0.533333      0.590476
support    2.000000  5.000000  0.571429   7.000000      7.000000
```

## 4. Conclusions
The comparison of classifier performance yields the following insights:

1. While all classifiers show relatively high accuracy on the full training set, this may indicate potential overfitting.

2. 7-fold cross-validation provides a more realistic performance assessment, revealing clearer differences between classifiers.

3. The 50% split evaluation helps assess generalization capability and predict real-world performance.

## 5. Visualization
A comparative visualization of classifier performance has been saved as `classifier_comparison.png`.
This graph allows comparison of accuracy across different evaluation methods for each classifier.
