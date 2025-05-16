# Numerical Summaries and Data Visualization

## 2.1 Summarizing Numerical Data

In statistical analysis, we often need to summarize and understand numerical variables. Unlike categorical variables (such as area codes or zip codes), numerical variables allow us to meaningfully calculate differences between values. Let's explore various techniques for summarizing numerical data using real examples.

### 2.1.1 Scatterplots for Paired Data

A **scatterplot** provides a case-by-case view of data for two numerical variables. For example:

- In the loan50 dataset, we can examine the relationship between:
  - Total income of borrowers (`total_income`)
  - Amount borrowed (`loan_amount`)

Each point in a scatterplot represents a single case. With 50 cases in loan50, there are 50 points plotted.

Key characteristics of scatterplots:

- Shows relationships between two variables
- Each point represents one observation
- Helps identify patterns and outliers
- Useful for detecting trends

### 2.1.2 Dot Plots and the Mean

Sometimes analyzing one variable at a time is more appropriate. A **dot plot** provides the most basic display for a single variable. For example:

- Interest rates for 50 loans can be displayed on a single axis
- Points are stacked when multiple observations share similar values
- The mean can be indicated (often with a different symbol)

### 2.1.3 Histograms and Shape

While dot plots show exact values, they become less practical with larger datasets. **Histograms** offer a more scalable alternative by:

- Grouping data into bins
- Showing frequency of observations in each bin
- Revealing the shape of the distribution

Common distribution shapes:

- **Right skewed**: Data trails off to the right
- **Left skewed**: Data trails off to the left
- **Symmetric**: Equal trailing on both sides

### 2.1.4 Variance and Standard Deviation

The mean helps describe the center of a dataset, but we also need to understand variability. Two key measures are:

1. **Variance**: Average of squared deviations from the mean
2. **Standard Deviation**: Square root of variance

These measures help us understand:

- How spread out the data is
- Typical distance of observations from the mean
- Reliability of the mean as a summary statistic

### 2.1.5 Box Plots, Quartiles, and the Median

A **box plot** provides a five-number summary of data:

- Minimum value
- First quartile (Q1)
- Median
- Third quartile (Q3)
- Maximum value

Additional features:

- Shows outliers as individual points
- Displays the interquartile range (IQR)
- Helps identify skewness and unusual values

### 2.1.6 Robust Statistics

Some statistical measures are more resistant to extreme values than others:

**Robust measures**:

- Median
- Interquartile range (IQR)

**Less robust measures**:

- Mean
- Standard deviation

Understanding when to use each type of measure is crucial for accurate data analysis.

## Example: The loan50 Dataset

The loan50 dataset provides real-world examples of these concepts:

1. **Interest Rates**:

   - Mean: 11.57%
   - Median: 9.93%
   - Shows right-skewed distribution
   - Contains some high outliers

2. **Loan Amounts vs. Total Income**:
   - Positive correlation
   - More variation in loan amounts for higher incomes
   - Some outliers in both variables

## Key Takeaways

1. Different visualization methods serve different purposes:

   - Scatterplots for relationships between variables
   - Dot plots for small datasets
   - Histograms for larger datasets
   - Box plots for summary statistics

2. Consider both center and spread when describing data

3. Be aware of outliers and their impact on different measures

4. Choose appropriate statistics based on:
   - Data distribution
   - Presence of outliers
   - Size of the dataset
   - Purpose of the analysis

## 2.2 Analyzing Categorical Data

### 2.2.1 Contingency Tables and Proportions

Contingency tables help us understand relationships between categorical variables. Let's look at some real examples:

#### Example: Loan Applications and Homeownership

From the loans dataset (n=10,000), we examined:

- Application type (`app_type`): individual or joint
- Homeownership status: rent, mortgage, or own

The data showed:

```
                rent    mortgage    own    Total
individual     3496      3839     1170    8505
joint           362       950      183    1495
Total         3858      4789     1353    10000
```

### 2.2.2 Row and Column Proportions

#### Row Proportions Example

For individual applicants:

- 41.1% rent (3496/8505)
- 45.1% have a mortgage (3839/8505)
- 13.8% own their home (1170/8505)

For joint applicants:

- 24.2% rent
- 63.5% have a mortgage
- 12.2% own their home

#### Column Proportions Example

Among renters:

- 90.6% are individual applications
- 9.4% are joint applications

This pattern varies across homeownership categories, suggesting an association between application type and homeownership status.

#### Example: Email Spam Classification

A real-world application of contingency tables in data science:

```
            text    HTML    Total
spam         209     158      367
not spam     986    2568     3554
Total       1195    2726     3921
```

Key findings:

- 17.5% of plain text emails were spam (209/1195)
- Only 5.8% of HTML emails were spam (158/2726)
- This information alone isn't sufficient for spam classification

### 2.2.5 Data Visualization Comparison: Pie Charts vs. Bar Plots

While both can represent categorical data, each has its strengths:

**Pie Chart Advantages:**

- Gives quick overview of proportions
- Shows part-to-whole relationships
- Useful for high-level presentations

**Bar Plot Advantages:**

- Easier to compare values
- More precise visual comparison
- Better for detailed analysis

Example: Homeownership Distribution

```
Homeownership Breakdown:
- Rent: 38.6%
- Mortgage: 47.9%
- Own: 13.5%
```

## 2.3 Case Study: Malaria Vaccine Trial

### 2.3.1 Study Design and Results

A clinical trial of the PfSPZ malaria vaccine:

- Treatment group: 14 patients (vaccine)
- Control group: 6 patients (placebo)
- Follow-up: 19 weeks
- Exposure: Drug-sensitive malaria strain

Results:

```
              Infection    No Infection    Total
Vaccine           5             9           14
Placebo           6             0            6
Total            11             9           20
```

Key Findings:

- Infection rate in vaccine group: 35.7% (5/14)
- Infection rate in placebo group: 100% (6/6)
- Difference: 64.3%

### 2.3.2 Statistical Analysis and Simulation

To evaluate the vaccine's effectiveness, we considered two hypotheses:

**H₀ (Independence Model):**

- Treatment and outcome are independent
- Observed difference (64.3%) due to chance

**Hₐ (Alternative Model):**

- Treatment affects infection rates
- Vaccine provides protection against malaria

Simulation Results:

- 100 simulations conducted
- Only 2% showed differences ≥ 64.3% by chance
- Suggests strong evidence for vaccine effectiveness

### Key Statistical Concepts Demonstrated:

1. **Random Variation:**

   - Even with no real effect, we expect some differences
   - Small samples can show large random variations

2. **Evidence Evaluation:**

   - Consider both effect size and sample size
   - Look for patterns that are unlikely due to chance

3. **Practical Significance:**

   - Statistical significance ≠ practical importance
   - Consider context and real-world implications

4. **Study Design Importance:**
   - Randomization helps control for confounding
   - Sample size affects reliability of conclusions

# Chapter Exercises - Data Visualization and Statistical Analysis

## 2.27 Make-up Exam

**Question**:
In a class of 25 students, 24 took an exam in class, and 1 student took a make-up exam the following day. The professor graded the first batch of 24 exams and found an average score of 74 points with a standard deviation of 8.9 points. The student who took the make-up exam scored 64 points.

(a) Does the new student's score increase or decrease the average score?
(b) What is the new average?
(c) Does the new student's score increase or decrease the standard deviation of the scores?

**Answer**:
(a) Decreases the average.

- The new score (64) is lower than the current mean (74), so it will pull the average down.

(b) Calculation of the new average:

```
Original total = 74 × 24 = 1,776 points
New student's score = 64 points
Total sum = 1,776 + 64 = 1,840 points
New average = 1,840 ÷ 25 = 73.6 points
```

(c) Increases the standard deviation.

- The new score (64) deviates significantly from the mean, increasing the overall variability.

## 2.28 Infant Mortality

**Question**:
The infant mortality rate is defined as the number of infant deaths per 1,000 live births. The relative frequency histogram shows the distribution of estimated infant death rates for 224 countries in 2014.

(a) Estimate Q1, the median, and Q3 from the histogram.
(b) Would you expect the mean of this data set to be smaller or larger than the median? Explain your reasoning.

**Answer**:
(a) Estimates from the histogram:

- Q1 ≈ 10 (deaths/1,000 births)
- Median ≈ 20 (deaths/1,000 births)
- Q3 ≈ 40 (deaths/1,000 births)

(b) The mean would be larger than the median.
Reasoning:

- The data is strongly right-skewed
- A few countries with very high mortality rates pull the mean upward
- The median is resistant to these extreme values

## 2.29 TV Watchers

**Question**:
Students in an AP Statistics class were asked how many hours of television they watch per week (including online streaming). This sample yielded an average of 4.71 hours, with a standard deviation of 4.18 hours. Is the distribution of number of hours students watch television weekly symmetric? If not, what shape would you expect this distribution to have?

**Answer**:
The distribution is likely not symmetric but right-skewed.

Reasoning:

1. TV watching time cannot be negative (lower bound at 0)
2. The mean (4.71) and standard deviation (4.18) being close suggests a long right tail
3. Some students likely watch much more TV than others, creating right skewness

## 2.30 A New Statistic

**Question**:
The statistic mean/median can be used as a measure of skewness. For a distribution where all observations are positive (xi > 0), what is the expected shape under the following conditions?

(a) mean/median = 1
(b) mean/median < 1
(c) mean/median > 1

**Answer**:
(a) mean/median = 1

- Perfectly symmetric distribution
- Mean equals median
- Example: Normal distribution

(b) mean/median < 1

- Left-skewed distribution
- Outliers on the left side
- Median greater than mean

(c) mean/median > 1

- Right-skewed distribution
- Outliers on the right side
- Mean greater than median

## 2.31 Oscar Winners

**Question**:
Compare the age distributions for all best actor and best actress winners from 1929 to 2018.

**Answer**:
Key comparisons:

1. Central Tendency:

   - Best Actress mean age: 36.2 years
   - Best Actor mean age: 43.8 years
   - Males typically 7.6 years older

2. Variability:

   - Best Actress SD: 11.9 years
   - Best Actor SD: 8.83 years
   - Greater variability in actress ages

3. Distribution Shape:

   - Actresses: Concentrated in younger ages, right-skewed
   - Actors: More symmetric, concentrated in middle age

4. Notable Trends:
   - Actresses win at younger ages
   - Actors win in middle age
   - Reflects industry age-gender dynamics

## 2.32 Exam Scores

**Question**:
The average on a history exam (scored out of 100 points) was 85, with a standard deviation of 15. Is the distribution of the scores symmetric?

**Answer**:
The distribution is likely left-skewed (negatively skewed).

Reasoning:

1. Maximum score ceiling (100 points)
2. High mean (85) limits right-side spread
3. Standard deviation implications:
   - Mean + 1SD = 100 (hits ceiling)
   - Mean - 1SD = 70
   - Creates compression at high scores

## 2.33 Stats Scores

**Question**:
Final exam scores of twenty introductory statistics students:
57, 66, 69, 71, 72, 73, 74, 77, 78, 78, 79, 79, 81, 81, 82, 83, 83, 88, 89, 94

Five-number summary:

- Min: 57
- Q1: 72.5
- Median: 78.5
- Q3: 82.5
- Max: 94

**Answer**:
Box plot characteristics:

1. Center: Distribution centered at median 78.5
2. IQR: 82.5 - 72.5 = 10 points
3. Asymmetry:
   - Left side of box (Q1 to median) slightly longer
   - Left whisker longer than right
4. Outliers:
   - Potential low outlier at 57
   - No clear high outliers

## 2.34 Marathon Winners

**Question**:
Analyze the distribution of finishing times for male and female winners of the New York Marathon between 1970 and 1999.

(a) What features are apparent in the histogram vs. box plot?
(b) What explains the bimodal distribution?
(c) Compare male and female time distributions
(d) What trends are visible in the time series plot?

**Answer**:
(a) Visualization differences:

- Histogram shows frequency distribution and overall shape
- Box plot reveals outliers and quartile positions

(b) Bimodal distribution cause:

- Clear separation between male and female times
- Natural result of physiological differences

(c) Gender comparison:

- Men: Faster times, less variability
- Women: Slower times, more spread

(d) Time series trends:

- Both genders show improvement
- Rapid improvement in 1970s
- Gradual improvement post-1980
- Gender gap gradually narrowing

# Quiz Solutions and Visual Analysis Insights

## Understanding Data Through Multiple Lenses

### Quiz 2.27: Make-up Exam Analysis

This problem demonstrates how a single data point can affect both central tendency and spread. The solution shows that:

- Adding a value below the mean (64 < 74) naturally decreases the average
- The deviation from the mean increases variability (standard deviation)
- This illustrates why both measures (mean and SD) are needed for full understanding

### Quiz 2.28: Infant Mortality Distribution

This example perfectly illustrates why visual representation is crucial:

- The histogram reveals the right-skewed nature of the data
- Numerical summaries alone might miss the important context of global health inequality
- The visual representation makes the disparity between countries immediately apparent

### Quiz 2.29: TV Watching Habits

This case demonstrates the importance of considering natural constraints:

- Time can't be negative, creating a boundary at zero
- The relationship between mean and SD suggests right skew
- Visual representation would help identify potential outliers in viewing habits

### Quiz 2.30: Skewness Measures

This theoretical exercise shows how different statistical measures relate to distribution shapes:

- The mean/median ratio provides a simple measure of skewness
- Visual representation would help validate these relationships
- Understanding these relationships helps in choosing appropriate analysis methods

### Quiz 2.31: Oscar Winners Age Analysis

This example showcases the power of comparative visualization:

- Age distributions reveal gender-based patterns
- Multiple visualization methods (histograms and summary statistics) tell a complete story
- Industry trends become apparent through visual analysis

### Quiz 2.32: Exam Score Distribution

This case illustrates how natural limits affect distribution:

- The 100-point maximum creates a ceiling effect
- Visual representation would show compression at the upper end
- Understanding these constraints is crucial for proper interpretation

### Quiz 2.33: Statistics Scores Analysis

This example demonstrates the value of different visualization methods:

- Raw data provides detail but can be overwhelming
- Five-number summary gives structure
- Box plot visualizes the distribution efficiently

### Quiz 2.34: Marathon Times Analysis

This case shows how different visualization methods reveal different aspects:

- Histograms show overall distribution
- Box plots reveal outliers
- Time series plots show temporal trends
- Each visualization adds unique insights

## Critical Considerations in Data Visualization

### When Visuals Offer Superior Insights

1. Pattern Recognition:

   - Humans are naturally better at recognizing patterns visually
   - Complex relationships become apparent through visualization
   - Trends and cycles are more easily identified

2. Outlier Detection:

   - Visual representations make unusual values immediately apparent
   - Context is maintained while identifying anomalies
   - Multiple outliers can be assessed simultaneously

3. Distribution Understanding:

   - Shape characteristics are instantly visible
   - Multimodality is easily detected
   - Skewness and symmetry become obvious

4. Comparative Analysis:
   - Side-by-side comparisons are more intuitive
   - Group differences are more apparent
   - Changes over time are clearer

### Complementary Use of Numerical and Visual Approaches

1. Initial Exploration:

   - Start with visual inspection for overall patterns
   - Follow up with precise numerical analysis
   - Use both to form comprehensive understanding

2. Validation:

   - Visual patterns can confirm numerical findings
   - Numerical analysis can quantify visual observations
   - Discrepancies between the two can reveal issues

3. Communication:
   - Visuals make presentations more engaging
   - Numbers provide precise support
   - Combined approach reaches diverse audiences

### Potential Pitfalls in Visualization Choice

1. Misleading Representations:

   - Inappropriate scales can distort relationships
   - 3D effects can obscure true patterns
   - Color choices can affect interpretation

2. Overcomplexity:

   - Too many variables in one visualization
   - Unnecessary decorative elements
   - Information overload

3. Inappropriate Choice of Plot:

   - Pie charts for too many categories
   - Line plots for unordered categories
   - Bar charts for continuous data

4. Context Omission:
   - Missing axis labels
   - Undefined units
   - Lack of reference points

### Best Practices for Combined Analysis

1. Systematic Approach:

   - Begin with clear questions
   - Choose appropriate visualization methods
   - Support with relevant statistics

2. Multiple Perspectives:

   - Use different visualization types
   - Compare with numerical summaries
   - Consider alternative representations

3. Iterative Refinement:

   - Start simple and add complexity as needed
   - Refine based on audience feedback
   - Maintain clarity throughout

4. Documentation:
   - Record visualization choices
   - Note any data transformations
   - Document interpretation rationale
