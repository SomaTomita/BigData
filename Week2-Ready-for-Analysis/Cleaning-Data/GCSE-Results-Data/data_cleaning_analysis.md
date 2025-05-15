# GCSE Results Data Cleaning Analysis

## Data Overview

The dataset contains GCSE exam results from UK students in the 1990s. Each record includes personal information (name, gender, date of birth, location) and exam results for up to 5 subjects with their corresponding grades.

## Step 1: Data Problems and Solutions

### 1. Missing Values

- **Problem**: Several types of missing values exist:
  - Empty firstname fields (marked as just comma)
  - Empty lastname fields (marked as comma)
  - Missing grades (marked as empty strings between commas)
  - Missing subjects (empty strings)
- **Solution Rule**:
  - For names: Mark as "UNKNOWN" if missing
  - For grades and subjects: Mark as "NA" to explicitly indicate missing data

### 2. Date Format Inconsistencies

- **Problem**: Multiple date formats are used:
  - ISO format (YYYY/MM/DD)
  - DD/MM/YYYY format
  - YYYY/Mon/DD format (using month abbreviations)
  - Some dates have invalid values (e.g., 1977/11/31 - November has 30 days)
- **Solution Rule**:
  - Standardize all dates to ISO format (YYYY-MM-DD)
  - Fix invalid dates by adjusting to the last valid day of the month
  - Flag any dates outside reasonable range (e.g., birth years before 1970 or after 1980)

### 3. Gender Field Issues

- **Problem**: Inconsistent gender coding:
  - 'm' for male
  - 'f' for female
  - 'mf' appears in some records
  - 'x' in some records
  - Empty values
- **Solution Rule**:
  - Standardize to 'M' and 'F'
  - Create new category 'O' for 'x' (Other/Non-binary)
  - Use 'U' for unknown/empty values
  - Flag 'mf' entries for manual review as they may be data entry errors

### 4. Grade Format Issues

- **Problem**: Inconsistent grade formats:
  - Letter grades (A\*, A+, A, B, C, D, E, F, G, U)
  - Numeric grades (0-7)
  - Invalid grades (K, N)
- **Solution Rule**:
  - Standardize all grades to the official GCSE grading scheme
  - Convert numeric grades to their letter equivalents where possible
  - Mark invalid grades as "Invalid"
  - Flag records with invalid grades for review

### 5. Subject Name Inconsistencies

- **Problem**: Same subjects written differently or with inconsistent quotes:
  - Some subjects in single quotes
  - Some subjects without quotes
  - Same subject appearing multiple times for same student
- **Solution Rule**:
  - Remove unnecessary quotes
  - Standardize subject names
  - Flag duplicate subject entries for same student

### 6. Data Validation Issues

- **Problem**: Some records have logically inconsistent data:
  - Same student taking same subject multiple times with different grades
  - Unrealistic birth dates
  - Missing mandatory fields
- **Solution Rule**:
  - Create validation rules for each field
  - Flag records violating these rules
  - Create separate log of problematic records for manual review

## Implementation Steps

1. Data Loading and Initial Assessment

   - Load data into appropriate data structure
   - Count occurrences of each type of issue
   - Generate summary statistics

2. Data Cleaning Pipeline

   - Implement each solution rule in sequence
   - Log all changes made to data
   - Keep original data intact for reference

3. Quality Assurance

   - Verify all dates are in correct format
   - Confirm all gender values are standardized
   - Check grade values against official GCSE scheme
   - Validate subject names are consistent

4. Documentation
   - Record all changes made to data
   - Note any records requiring manual review
   - Document any assumptions made during cleaning

## Additional Considerations

- The cleaning process should be reproducible
- All transformations should be documented
- Original data should be preserved
- Create separate clean dataset rather than modifying original
- Consider creating a data quality report showing before/after statistics

This analysis provides a framework for cleaning the GCSE results data while maintaining data integrity and transparency in the cleaning process.

# Analysis of Results

```
Data cleaning completed. Output saved to Week2-Ready-for-Analysis/Cleaning-Data/GCSE-Results-Data/gcse_cleaned.csv

Summary:
Total records: 115
Records with unknown names: 7
Records with invalid dates: 3
Records with invalid grades: 19
Records with duplicate subjects: 14
```

1. **Dataset Size and Overall Quality**

   - Total dataset contains 115 student records
   - Approximately 37% of records (43 records) have some form of data quality issue
   - Despite issues, majority of records (63%) are clean and usable

2. **Missing Name Information (7 records)**

   - 6% of records have missing names
   - This could impact:
     - Student identification
     - Demographic analysis
     - Record matching/deduplication
   - Solution applied: Marked as "UNKNOWN" to maintain data structure while flagging missing information

3. **Date Format Issues (3 records)**

   - Only 2.6% of records have invalid dates
   - Issues found:
     - Invalid dates (e.g., November 31st)
     - Inconsistent formats (mixing DD/MM/YYYY with YYYY/MM/DD)
   - Relatively low impact on overall dataset quality
   - Successfully standardized 97.4% of dates to ISO format

4. **Grade Quality Issues (19 records)**

   - 16.5% of records have invalid grades
   - Most significant data quality issue in the dataset
   - Problems include:
     - Non-standard grade notations
     - Numeric grades requiring conversion
     - Invalid grade symbols
   - Impact: Could affect grade distribution analysis and performance metrics

5. **Subject Duplication (14 records)**
   - 12.2% of records have duplicate subject entries
   - Potential causes:
     - Data entry errors
     - Multiple exam attempts
     - System migration issues
   - Impact: Could skew subject popularity statistics and student performance analysis

### Recommendations for Further Improvement

1. **Name Data Quality**

   - Implement stricter data entry validation
   - Consider making first and last names mandatory fields
   - Add name format standardization rules

2. **Date Standardization**

   - Enforce single date format at data entry
   - Add real-time date validation
   - Consider adding age validation based on reasonable ranges

3. **Grade Standardization**

   - Create comprehensive grade mapping system
   - Implement grade validation at entry point
   - Document all grade conversion rules
   - Consider adding grade verification process

4. **Subject Entry Improvement**
   - Implement dropdown subject selection to prevent duplicates
   - Add warning system for duplicate subject entries
   - Consider adding logic to handle multiple exam attempts

### Impact on Analysis

The cleaned dataset provides a reliable foundation for analysis, with some considerations:

1. **Statistical Analysis**

   - Remove or separately analyze records with invalid grades
   - Consider weighted analysis to account for data quality issues
   - Document assumptions made during cleaning process

2. **Performance Metrics**

   - Calculate metrics both with and without problematic records
   - Note potential bias from excluded records
   - Consider confidence intervals based on data quality

3. **Reporting**
   - Include data quality metrics in all reports
   - Document cleaning decisions and their impact
   - Maintain transparency about data limitations

This cleaning process has successfully standardized the dataset while preserving its analytical value, though users should be aware of the noted limitations when drawing conclusions from the data.
