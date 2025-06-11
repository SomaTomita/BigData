# SQL Exercises and Query Results

## Sample Database Tables

### STUDENT Table

| studentId | firstName | lastName | Gender | Dob        | auth       |
| --------- | --------- | -------- | ------ | ---------- | ---------- |
| 1         | John      | Smith    | M      | 2000-05-15 | Birmingham |
| 2         | Emma      | Williams | F      | 2001-03-22 | London     |
| 3         | Sam       | Brown    | M      | 2000-07-30 | London     |
| 4         | Sarah     | Johnson  | F      | 2001-11-08 | Manchester |
| 5         | Michael   | Davis    | M      | 2000-09-12 | Birmingham |
| 6         | Lucy      | Wilson   | F      | 2001-01-25 | London     |

### SUBJECT Table

| subjectId | subjectName | board   |
| --------- | ----------- | ------- |
| 101       | Mathematics | AQA     |
| 102       | Physics     | OCR     |
| 103       | Chemistry   | AQA     |
| 104       | History     | Edexcel |
| 105       | Biology     | OCR     |

### ENROLL Table

| studentId | subjectId | grade |
| --------- | --------- | ----- |
| 1         | 101       | B     |
| 1         | 104       | A     |
| 2         | 101       | A\*   |
| 3         | 103       | B     |
| 4         | 104       | A     |
| 5         | 101       | U     |
| 6         | 101       | A     |
| 6         | 104       | B     |

## Exercise 1: Get all student details ordered by auth

### Query:

```sql
SELECT * FROM STUDENT ORDER BY auth;
```

### Result:

| studentId | firstName | lastName | Gender | Dob        | auth       |
| --------- | --------- | -------- | ------ | ---------- | ---------- |
| 1         | John      | Smith    | M      | 2000-05-15 | Birmingham |
| 5         | Michael   | Davis    | M      | 2000-09-12 | Birmingham |
| 2         | Emma      | Williams | F      | 2001-03-22 | London     |
| 3         | Sam       | Brown    | M      | 2000-07-30 | London     |
| 6         | Lucy      | Wilson   | F      | 2001-01-25 | London     |
| 4         | Sarah     | Johnson  | F      | 2001-11-08 | Manchester |

## Exercise 2: Group by auth with count

### Query:

```sql
SELECT COUNT(*) as student_count, auth
FROM STUDENT
GROUP BY auth;
```

### Result:

| student_count | auth       |
| ------------- | ---------- |
| 2             | Birmingham |
| 3             | London     |
| 1             | Manchester |

## Exercise 3: Count enrollments per subject

### Query:

```sql
SELECT COUNT(e.subjectId) as enrollment_count, s.subjectName
FROM ENROLL e, SUBJECT s
WHERE e.subjectId = s.subjectId
GROUP BY s.subjectId;
```

### Result:

| enrollment_count | subjectName |
| ---------------- | ----------- |
| 4                | Mathematics |
| 0                | Physics     |
| 1                | Chemistry   |
| 3                | History     |
| 0                | Biology     |

## Exercise 4: Students taking History

### Query:

```sql
SELECT s.lastName, s.studentId, sub.subjectName
FROM STUDENT s, ENROLL e, SUBJECT sub
WHERE s.studentId = e.studentId
AND e.subjectId = sub.subjectId
AND sub.subjectName = 'History';
```

### Result:

| lastName | studentId | subjectName |
| -------- | --------- | ----------- |
| Smith    | 1         | History     |
| Johnson  | 4         | History     |
| Wilson   | 6         | History     |

## Exercise 5: Students with 'U' grade in Mathematics

### Query:

```sql
SELECT s.lastName, s.studentId, sub.subjectName, e.grade
FROM STUDENT s, ENROLL e, SUBJECT sub
WHERE s.studentId = e.studentId
AND e.subjectId = sub.subjectId
AND sub.subjectName = 'Mathematics'
AND e.grade = 'U';
```

### Result:

| lastName | studentId | subjectName | grade |
| -------- | --------- | ----------- | ----- |
| Davis    | 5         | Mathematics | U     |

## Exercise 6: Complete Student Data (Denormalized)

### Query:

```sql
SELECT s.*, sub.subjectName, e.grade
FROM STUDENT s, ENROLL e, SUBJECT sub
WHERE s.studentId = e.studentId
AND e.subjectId = sub.subjectId;
```

### Result:

| studentId | firstName | lastName | Gender | Dob        | auth       | subjectName | grade |
| --------- | --------- | -------- | ------ | ---------- | ---------- | ----------- | ----- |
| 1         | John      | Smith    | M      | 2000-05-15 | Birmingham | Mathematics | B     |
| 1         | John      | Smith    | M      | 2000-05-15 | Birmingham | History     | A     |
| 2         | Emma      | Williams | F      | 2001-03-22 | London     | Mathematics | A\*   |
| 3         | Sam       | Brown    | M      | 2000-07-30 | London     | Chemistry   | B     |
| 4         | Sarah     | Johnson  | F      | 2001-11-08 | Manchester | History     | A     |
| 5         | Michael   | Davis    | M      | 2000-09-12 | Birmingham | Mathematics | U     |
| 6         | Lucy      | Wilson   | F      | 2001-01-25 | London     | Mathematics | A     |
| 6         | Lucy      | Wilson   | F      | 2001-01-25 | London     | History     | B     |

## Exercise 7: Gender Analysis (Female Students)

### Query:

```sql
SELECT s.*, sub.subjectName, e.grade
FROM STUDENT s, ENROLL e, SUBJECT sub
WHERE s.studentId = e.studentId
AND e.subjectId = sub.subjectId
AND s.Gender = 'F';
```

### Result:

| studentId | firstName | lastName | Gender | Dob        | auth       | subjectName | grade |
| --------- | --------- | -------- | ------ | ---------- | ---------- | ----------- | ----- |
| 2         | Emma      | Williams | F      | 2001-03-22 | London     | Mathematics | A\*   |
| 4         | Sarah     | Johnson  | F      | 2001-11-08 | Manchester | History     | A     |
| 6         | Lucy      | Wilson   | F      | 2001-01-25 | London     | Mathematics | A     |
| 6         | Lucy      | Wilson   | F      | 2001-01-25 | London     | History     | B     |

### Analysis Summary:

From the gender-based analysis, we can observe:

1. Female students (3 students, 4 enrollments)

   - Average grade distribution: A\*/A: 75%, B: 25%
   - Most popular subjects: Mathematics and History
   - No failing grades (U)

2. Male students (3 students, 4 enrollments)
   - Average grade distribution: A: 25%, B: 50%, U: 25%
   - More diverse subject choices (Mathematics, History, Chemistry)
   - One failing grade in Mathematics

This data suggests that female students in the sample are performing slightly better overall, with higher average grades and no failing marks. However, the sample size is small, so these differences may not be statistically significant.

# SQL Aggregate Functions and Clauses

## Basic Aggregate Functions

### COUNT

Counts the number of rows or non-null values.

```sql
-- Count all rows
SELECT COUNT(*) FROM STUDENT;

-- Count students by gender
SELECT Gender, COUNT(*) as student_count
FROM STUDENT
GROUP BY Gender;

-- Count non-null values in a column
SELECT COUNT(grade) as grades_given
FROM ENROLL;
```

### AVG, SUM, MIN, MAX

Calculate average, sum, minimum, and maximum values.

```sql
-- Basic usage
SELECT
    AVG(numeric_grade) as average,
    SUM(numeric_grade) as total,
    MIN(numeric_grade) as lowest,
    MAX(numeric_grade) as highest
FROM grades;

-- Practical example with CASE
SELECT subjectName,
    AVG(CASE
        WHEN grade = 'A*' THEN 5
        WHEN grade = 'A' THEN 4
        WHEN grade = 'B' THEN 3
        ELSE 1
    END) as avg_grade_points
FROM ENROLL e
JOIN SUBJECT s ON e.subjectId = s.subjectId
GROUP BY subjectName;
```

## Important SQL Clauses

### GROUP BY

Groups rows that have the same values in specified columns.

```sql
-- Basic grouping
SELECT auth, COUNT(*) as student_count
FROM STUDENT
GROUP BY auth;

-- Multiple column grouping
SELECT auth, Gender, COUNT(*) as count
FROM STUDENT
GROUP BY auth, Gender;
```

### HAVING

Filters groups based on aggregate conditions (used with GROUP BY).

```sql
-- Find subjects with more than 2 students
SELECT subjectName, COUNT(*) as student_count
FROM ENROLL e
JOIN SUBJECT s ON e.subjectId = s.subjectId
GROUP BY subjectName
HAVING COUNT(*) > 2;

-- Find authorities with high average grades
SELECT auth, AVG(numeric_grade) as avg_grade
FROM grades
GROUP BY auth
HAVING AVG(numeric_grade) > 3.5;
```

### CASE

Provides conditional logic in SQL queries.

```sql
-- Simple CASE
SELECT firstName, lastName,
    CASE Gender
        WHEN 'M' THEN 'Male'
        WHEN 'F' THEN 'Female'
        ELSE 'Other'
    END as gender_description
FROM STUDENT;

-- Searched CASE
SELECT firstName, lastName, grade,
    CASE
        WHEN grade = 'A*' THEN 'Outstanding'
        WHEN grade IN ('A', 'B') THEN 'Good'
        WHEN grade = 'U' THEN 'Needs Improvement'
        ELSE 'Average'
    END as performance
FROM STUDENT s
JOIN ENROLL e ON s.studentId = e.studentId;
```

### WITH (Common Table Expression - CTE)

Creates a named temporary result set that you can reference within a SELECT, INSERT, UPDATE, DELETE, or MERGE statement.

```sql
-- Basic CTE
WITH StudentGrades AS (
    SELECT s.firstName, s.lastName,
           COUNT(*) as subjects_taken,
           AVG(CASE
               WHEN grade = 'A*' THEN 5
               WHEN grade = 'A' THEN 4
               WHEN grade = 'B' THEN 3
               ELSE 1
           END) as avg_grade
    FROM STUDENT s
    JOIN ENROLL e ON s.studentId = e.studentId
    GROUP BY s.firstName, s.lastName
)
SELECT * FROM StudentGrades
WHERE avg_grade > 3.0;

-- Multiple CTEs
WITH
HighPerformers AS (
    SELECT studentId
    FROM ENROLL
    WHERE grade IN ('A*', 'A')
),
SubjectCounts AS (
    SELECT studentId, COUNT(*) as subject_count
    FROM ENROLL
    GROUP BY studentId
)
SELECT s.firstName, s.lastName, sc.subject_count
FROM STUDENT s
JOIN SubjectCounts sc ON s.studentId = sc.studentId
WHERE s.studentId IN (SELECT studentId FROM HighPerformers);
```

## Key Points to Remember

1. **Aggregate Functions**

   - Always used with GROUP BY (except when calculating over entire table)
   - Can't mix aggregate and non-aggregate columns without GROUP BY
   - NULL values are typically ignored in calculations

2. **GROUP BY**

   - Must include all non-aggregate columns in SELECT list
   - Executes after WHERE but before HAVING
   - Can group by multiple columns

3. **HAVING**

   - Filters groups, not individual rows
   - Can only use aggregate functions or GROUP BY columns
   - Executes after GROUP BY

4. **CASE**

   - Can be used in SELECT, WHERE, GROUP BY, and HAVING clauses
   - Simple CASE compares equality
   - Searched CASE allows for complex conditions

5. **WITH**
   - Makes complex queries more readable
   - Can reference previous CTEs in the same WITH clause
   - Helps break down complex problems into smaller steps

# Advanced JOIN Examples

### Understanding Different JOIN Types

1. **INNER JOIN**: Returns only the matching rows between tables
2. **LEFT JOIN**: Returns all rows from the left table and matching rows from the right table
3. **RIGHT JOIN**: Returns all rows from the right table and matching rows from the left table
4. **FULL JOIN**: Returns all rows from both tables, matching where possible

### Exercise 8: Compare INNER JOIN vs LEFT JOIN

#### Query with INNER JOIN:

```sql
SELECT s.firstName, s.lastName, sub.subjectName, e.grade
FROM STUDENT s
INNER JOIN ENROLL e ON s.studentId = e.studentId
INNER JOIN SUBJECT sub ON e.subjectId = sub.subjectId;
```

#### Result (INNER JOIN):

| firstName | lastName | subjectName | grade |
| --------- | -------- | ----------- | ----- |
| John      | Smith    | Mathematics | B     |
| John      | Smith    | History     | A     |
| Emma      | Williams | Mathematics | A\*   |
| Sam       | Brown    | Chemistry   | B     |
| Sarah     | Johnson  | History     | A     |
| Michael   | Davis    | Mathematics | U     |
| Lucy      | Wilson   | Mathematics | A     |
| Lucy      | Wilson   | History     | B     |

#### Query with LEFT JOIN:

```sql
SELECT s.firstName, s.lastName, sub.subjectName, e.grade
FROM STUDENT s
LEFT JOIN ENROLL e ON s.studentId = e.studentId
LEFT JOIN SUBJECT sub ON e.subjectId = sub.subjectId;
```

#### Result (LEFT JOIN):

| firstName | lastName | subjectName | grade |
| --------- | -------- | ----------- | ----- |
| John      | Smith    | Mathematics | B     |
| John      | Smith    | History     | A     |
| Emma      | Williams | Mathematics | A\*   |
| Sam       | Brown    | Chemistry   | B     |
| Sarah     | Johnson  | History     | A     |
| Michael   | Davis    | Mathematics | U     |
| Lucy      | Wilson   | Mathematics | A     |
| Lucy      | Wilson   | History     | B     |

Note: In this specific example, both queries return the same results because all students have enrollments. Let's see a more illustrative example.

### Exercise 9: Finding Students Not Enrolled in Any Subject

```sql
SELECT s.firstName, s.lastName,
       COALESCE(sub.subjectName, 'Not Enrolled') as subject_status
FROM STUDENT s
LEFT JOIN ENROLL e ON s.studentId = e.studentId
LEFT JOIN SUBJECT sub ON e.subjectId = sub.subjectId
WHERE e.studentId IS NULL;
```

### Exercise 10: Complex JOIN with Multiple Conditions

```sql
SELECT
    s.firstName,
    s.lastName,
    COUNT(DISTINCT e.subjectId) as subjects_enrolled,
    STRING_AGG(sub.subjectName, ', ') as subjects,
    AVG(CASE
        WHEN e.grade = 'A*' THEN 5
        WHEN e.grade = 'A' THEN 4
        WHEN e.grade = 'B' THEN 3
        WHEN e.grade = 'C' THEN 2
        WHEN e.grade = 'U' THEN 0
        ELSE 1
    END) as avg_grade_points
FROM STUDENT s
LEFT JOIN ENROLL e ON s.studentId = e.studentId
LEFT JOIN SUBJECT sub ON e.subjectId = sub.subjectId
GROUP BY s.studentId, s.firstName, s.lastName
HAVING COUNT(DISTINCT e.subjectId) > 1
ORDER BY avg_grade_points DESC;
```

#### Result:

| firstName | lastName | subjects_enrolled | subjects             | avg_grade_points |
| --------- | -------- | ----------------- | -------------------- | ---------------- |
| John      | Smith    | 2                 | Mathematics, History | 3.5              |
| Lucy      | Wilson   | 2                 | Mathematics, History | 3.0              |

### Exercise 11: Analyzing Grade Distribution by Subject and Authority

```sql
WITH GradePoints AS (
    SELECT
        sub.subjectName,
        s.auth,
        CASE
            WHEN e.grade = 'A*' THEN 5
            WHEN e.grade = 'A' THEN 4
            WHEN e.grade = 'B' THEN 3
            WHEN e.grade = 'C' THEN 2
            WHEN e.grade = 'U' THEN 0
            ELSE 1
        END as grade_points
    FROM STUDENT s
    INNER JOIN ENROLL e ON s.studentId = e.studentId
    INNER JOIN SUBJECT sub ON e.subjectId = sub.subjectId
)
SELECT
    subjectName,
    auth,
    COUNT(*) as student_count,
    ROUND(AVG(grade_points), 2) as avg_grade,
    MIN(grade_points) as min_grade,
    MAX(grade_points) as max_grade
FROM GradePoints
GROUP BY subjectName, auth
ORDER BY subjectName, avg_grade DESC;
```

#### Result:

| subjectName | auth       | student_count | avg_grade | min_grade | max_grade |
| ----------- | ---------- | ------------- | --------- | --------- | --------- |
| Mathematics | London     | 2             | 4.50      | 4         | 5         |
| Mathematics | Birmingham | 2             | 1.50      | 0         | 3         |
| History     | London     | 1             | 3.00      | 3         | 3         |
| History     | Birmingham | 1             | 4.00      | 4         | 4         |
| History     | Manchester | 1             | 4.00      | 4         | 4         |
| Chemistry   | London     | 1             | 3.00      | 3         | 3         |

### Exercise 12: Finding Subject Pairs Often Taken Together

```sql
SELECT
    s1.subjectName as subject1,
    s2.subjectName as subject2,
    COUNT(*) as pair_count
FROM ENROLL e1
JOIN ENROLL e2 ON e1.studentId = e2.studentId AND e1.subjectId < e2.subjectId
JOIN SUBJECT s1 ON e1.subjectId = s1.subjectId
JOIN SUBJECT s2 ON e2.subjectId = s2.subjectId
GROUP BY s1.subjectName, s2.subjectName
HAVING COUNT(*) > 0
ORDER BY pair_count DESC;
```

#### Result:

| subject1    | subject2 | pair_count |
| ----------- | -------- | ---------- |
| Mathematics | History  | 2          |

This shows that Mathematics and History are most commonly taken together in our sample dataset.

### Key Differences Between JOIN Types:

1. **INNER JOIN**

   - Only returns matching rows
   - Useful when you want to ensure data exists in both tables
   - Most commonly used JOIN type

2. **LEFT JOIN**

   - Returns all rows from left table, even if no matches in right table
   - Useful for finding missing relationships
   - Good for checking completeness of data

3. **RIGHT JOIN**

   - Similar to LEFT JOIN but keeps all rows from right table
   - Less commonly used (can usually be rewritten as LEFT JOIN)

4. **FULL JOIN**
   - Combines both LEFT and RIGHT JOIN
   - Returns all rows from both tables
   - Useful for finding all possible relationships and gaps

The choice of JOIN type depends on your specific needs:

- Use INNER JOIN when you only want matching data
- Use LEFT/RIGHT JOIN when you need to preserve all records from one table
- Use FULL JOIN when you need to see all possible combinations and identify gaps
