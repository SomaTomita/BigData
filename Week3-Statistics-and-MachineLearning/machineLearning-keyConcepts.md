# Week 3: Key Concepts in Machine Learning

## From Descriptive to Predictive Analytics

The evolution of data analysis moves from describing what we see to predicting what might happen:

1. **Descriptive Analytics** (What happened?)

   - Summarizing data through statistics
   - Visualizing relationships
   - Example: Average customer spending per month

2. **Predictive Analytics** (What might happen?)
   - Using patterns to make predictions
   - Building classification/regression models
   - Example: Predicting which customers might churn next month

## What is Machine Learning?

Machine Learning is the study of algorithms that learn from data to make predictions or decisions without being explicitly programmed.

### Traditional Programming vs Machine Learning:

```
Traditional Programming:
Data + Rules = Output

Machine Learning:
Data + Output = Rules
```

### Real-world Example:

- **Traditional Email Filter**: Manually write rules like "if email contains 'win money' then mark as spam"
- **ML Email Filter**: Show the system thousands of examples of spam and non-spam emails, let it learn the patterns

## How Machine Learning Works

### Basic Process:

1. **Data Collection**: Gather relevant data with features and labels
2. **Data Preparation**: Clean and preprocess the data
3. **Training**: Algorithm learns patterns from training data
4. **Testing**: Evaluate model on unseen data
5. **Deployment**: Use model for predictions

### Concrete Example - Iris Classification:

- **Features**: Sepal length, sepal width, petal length, petal width
- **Label**: Species (setosa, versicolor, virginica)
- **Goal**: Learn to predict species from measurements

## Categories of Machine Learning

### 1. Supervised Learning

- Has labeled data
- Learns to predict outcomes

#### Examples:

- **Classification**:
  - Spam detection (Spam/Not Spam)
  - Disease diagnosis (Positive/Negative)
  - Credit approval (Approve/Deny)
- **Regression**:
  - House price prediction
  - Sales forecasting
  - Temperature prediction

### 2. Unsupervised Learning

- No labels
- Finds patterns/structure in data

#### Examples:

- **Clustering**:
  - Customer segmentation
  - Document grouping
  - Image segmentation

### 3. Reinforcement Learning

- Learning through trial and error
- Receives rewards/penalties

#### Examples:

- Game playing (Chess, Go)
- Robot navigation
- Resource management

## Key Terms and Concepts

### Data Splitting

- **Training Set** (60-80%): For model learning
- **Validation Set** (10-20%): For tuning
- **Test Set** (10-20%): For final evaluation

### Common Challenges

#### 1. Overfitting

- Model learns noise in training data
- Signs:
  - High training accuracy
  - Poor test accuracy

Example:

```
Training Accuracy: 99%
Test Accuracy: 65%
```

#### 2. Underfitting

- Model too simple to capture patterns
- Signs:
  - Poor performance on both training and test data

Example:

```
Training Accuracy: 70%
Test Accuracy: 68%
```

### Model Evaluation Metrics

1. **Accuracy**: Overall correctness
2. **Precision**: Accuracy of positive predictions
3. **Recall**: Ability to find all positive cases
4. **F1-Score**: Balance between precision and recall

## Real-world Considerations

### Concept Drift

- Model performance degrades over time
- Example: Customer behavior changes during economic shifts

### Best Practices

1. Regular model monitoring
2. Periodic retraining
3. Version control for models
4. Documentation of assumptions
5. Validation against business metrics

## Practical Example: Customer Churn Prediction

### Problem Setup:

- **Goal**: Predict which customers might leave
- **Features**:
  - Usage patterns
  - Customer service interactions
  - Payment history
  - Demographics
- **Label**: Churned (Yes/No)

### Process:

1. Collect historical customer data
2. Prepare and clean data
3. Split into training/validation/test sets
4. Train model
5. Evaluate performance
6. Deploy and monitor

### Typical Results:

```
Training Accuracy: 85%
Validation Accuracy: 82%
Test Accuracy: 81%
```

## Summary

Machine Learning enables us to:

1. Move from description to prediction
2. Automate decision-making
3. Find patterns in complex data
4. Adapt to new situations

Remember:

- Models need regular maintenance
- Quality data is crucial
- Business context matters
- Evaluation must be ongoing

## Practice Questions

### Question 1: Defining Machine Learning

**Which of the following are plausible definitions of "machine learning"?**

Options:

1. Ways for a machine to independently gain knowledge of a subject
2. Methods for making a computer improve its behaviour through experience
3. Automated techniques for finding patterns in data

**Answer:** All three options are plausible definitions of machine learning.

**Explanation:**

- Option 1 captures the autonomous learning aspect
- Option 2 emphasizes the improvement through experience, which is a key aspect of ML
- Option 3 describes the pattern recognition capability, which is fundamental to ML

### Question 2: Machine Learning vs Data Mining

**According to Witten et al, what is the main difference between "machine learning" and "data mining"?**

Options:

1. "Data mining" is what we are trying to do; "machine learning" refers to a range of techniques to achieve that goal
2. It is "data mining" if the volume of data being processed is very large, "machine learning" otherwise
3. It is "data mining" if the patterns learned are simple rules or statistical relationships, "machine learning" if they are more intricate and sophisticated
4. It is "data mining" if you are talking to a business audience, "machine learning" if you are talking to a scientific one

**Answer:** Option 1 is correct.

**Explanation:**
Data mining represents the goal or objective (finding valuable patterns in data), while machine learning provides the technical methods and approaches to achieve this goal. The distinction isn't about data volume, pattern complexity, or audience type.

### Question 3: Value of Comprehensible Models

**Why is it valuable for machine learning to produce comprehensible structural descriptions, rather than just black-box predictors?**

Options:

1. Because black box predictors tend to be slow to execute
2. Because they are then producing knowledge about the world that can be integrated with knowledge from other sources
3. Because black box predictors tend to produce less accurate answers
4. Because they allow humans to check if the described structure is possible and plausible

**Answer:** Options 2 and 4 are correct.

**Explanation:**

- Comprehensible models are valuable because they:
  - Provide interpretable knowledge that can be combined with other domain knowledge
  - Allow domain experts to validate the model's reasoning
  - Enable trust and understanding of the model's decisions
- The execution speed and accuracy are not inherently related to model interpretability

### Question 4: Machine Learning vs Statistics

**Which of these is a difference between "machine learning" and "statistics"?**

Options:

1. There is no clear, widely-agreed difference
2. "Statistics" deals with relatively simple patterns and rules; "machine learning" allows more complex relationships to be detected
3. "Statistics" is the term for techniques developed prior to about 1995; techniques developed since then are generally labelled "machine learning"

**Answer:** Option 1 is correct.

**Explanation:**
There is no clear consensus on the distinction between machine learning and statistics. Many techniques are shared between both fields, and the boundaries are often blurred. The difference is not about:

- Complexity of patterns (both fields can handle simple and complex relationships)
- Time period of development (both fields continue to evolve)
  Rather, they represent different perspectives and approaches to similar problems, with significant overlap in methods and goals.
