# SQL, Distributed Data Processing, and Hadoop Introduction

## Introduction to SQL

SQL (Structured Query Language) is the standard language for managing and manipulating relational databases. It provides a powerful set of tools for:

- Creating and modifying database structures (DDL - Data Definition Language)
- Manipulating data (DML - Data Manipulation Language)
- Querying and retrieving data
- Managing access control

## Database Fundamentals

### Sample Database Schema

Let's work with a practical example of a school database system:

```sql
-- Student table structure
CREATE TABLE STUDENT (
    studentId INT NOT NULL,
    firstName VARCHAR(45) NULL,
    lastName VARCHAR(45) NULL,
    Gender VARCHAR(1) NULL,
    Dob DATE NULL,
    auth VARCHAR(45) NULL,
    PRIMARY KEY (studentId)
);

-- Subject table structure
CREATE TABLE SUBJECT (
    subjectId INT NOT NULL,
    subjectName VARCHAR(45) NULL,
    board VARCHAR(45) NULL,
    PRIMARY KEY (subjectId)
);

-- Enrollment table structure
CREATE TABLE ENROLL (
    studentId INT NOT NULL,
    subjectId INT NOT NULL,
    grade VARCHAR(2) NULL,
    PRIMARY KEY (studentId, subjectId),
    FOREIGN KEY (studentId) REFERENCES STUDENT(studentId),
    FOREIGN KEY (subjectId) REFERENCES SUBJECT(subjectId)
);
```

### Sample Data

```sql
-- Sample Student Data
INSERT INTO STUDENT VALUES
(1, 'John', 'Smith', 'M', '2000-05-15', 'London'),
(2, 'Emma', 'Williams', 'F', '2001-03-22', 'Manchester'),
(3, 'Sam', 'Williams', 'M', '2000-07-30', 'London'),
(4, 'Sarah', 'Johnson', 'F', '2001-11-08', 'Birmingham');

-- Sample Subject Data
INSERT INTO SUBJECT VALUES
(101, 'Mathematics', 'AQA'),
(102, 'Physics', 'OCR'),
(103, 'Chemistry', 'AQA'),
(104, 'Biology', 'Edexcel');

-- Sample Enrollment Data
INSERT INTO ENROLL VALUES
(1, 101, 'A'),
(1, 102, 'B'),
(2, 101, 'A*'),
(3, 103, 'A'),
(4, 104, 'B+');
```

## SQL Queries and Operations

### Basic Queries

1. **Select all students:**

```sql
SELECT * FROM STUDENT;
```

2. **Select specific columns:**

```sql
SELECT firstName, lastName, auth
FROM STUDENT;
```

### Filtering with WHERE

```sql
-- Find all students from London
SELECT firstName, lastName
FROM STUDENT
WHERE auth = 'London';

-- Find students with grade 'A' or better
SELECT s.firstName, s.lastName, e.grade, sub.subjectName
FROM STUDENT s
JOIN ENROLL e ON s.studentId = e.studentId
JOIN SUBJECT sub ON e.subjectId = sub.subjectId
WHERE e.grade IN ('A', 'A*');
```

### Joins and Relationships

```sql
-- Show all student enrollments with subject names
SELECT
    s.firstName,
    s.lastName,
    sub.subjectName,
    e.grade
FROM STUDENT s
JOIN ENROLL e ON s.studentId = e.studentId
JOIN SUBJECT sub ON e.subjectId = sub.subjectId;
```

### Aggregation and Grouping

```sql
-- Count students per subject
SELECT
    sub.subjectName,
    COUNT(*) as student_count
FROM SUBJECT sub
JOIN ENROLL e ON sub.subjectId = e.subjectId
GROUP BY sub.subjectName
ORDER BY student_count DESC;

-- Average grades per subject (assuming numeric conversion)
SELECT
    sub.subjectName,
    COUNT(*) as total_students,
    AVG(CASE
        WHEN e.grade = 'A*' THEN 5
        WHEN e.grade = 'A' THEN 4
        WHEN e.grade = 'B' THEN 3
        WHEN e.grade = 'C' THEN 2
        ELSE 1
    END) as avg_grade
FROM SUBJECT sub
JOIN ENROLL e ON sub.subjectId = e.subjectId
GROUP BY sub.subjectName;
```

## Distributed Data Processing

Distributed data processing involves processing large datasets across multiple computers or nodes. Key concepts include:

1. **Data Partitioning**: Splitting data across multiple nodes
2. **Parallel Processing**: Processing data simultaneously on multiple nodes
3. **Fault Tolerance**: Handling node failures gracefully
4. **Data Locality**: Processing data where it's stored

### Example of Data Partitioning

Consider our student database distributed across multiple nodes:

```
Node 1: Students A-G
Node 2: Students H-M
Node 3: Students N-S
Node 4: Students T-Z
```

## Introduction to Hadoop

Hadoop is a framework for distributed storage and processing of big data. Key components include:

1. **HDFS (Hadoop Distributed File System)**

   - Distributed storage system
   - Replication for fault tolerance
   - Optimized for large files

2. **MapReduce**
   - Programming model for processing big data
   - Map phase: Parallel processing
   - Reduce phase: Aggregation of results

### Example MapReduce Job

Count students per educational authority:

```java
// Map function
public void map(LongWritable key, Text value, Context context) {
    String[] fields = value.toString().split(",");
    String auth = fields[5];  // authority field
    context.write(new Text(auth), new IntWritable(1));
}

// Reduce function
public void reduce(Text key, Iterable<IntWritable> values, Context context) {
    int sum = 0;
    for (IntWritable val : values) {
        sum += val.get();
    }
    context.write(key, new IntWritable(sum));
}
```

### Practical Use Cases

1. **Log Analysis**

   - Processing server logs across multiple data centers
   - Analyzing user behavior patterns

2. **Data Warehousing**

   - Storing historical student data
   - Analyzing academic performance trends

3. **Real-time Analytics**
   - Monitoring student performance
   - Identifying areas for intervention

## Best Practices

1. **SQL Query Optimization**

   - Use appropriate indexes
   - Write efficient joins
   - Avoid SELECT \*
   - Use EXPLAIN PLAN

2. **Distributed Processing**

   - Choose appropriate partitioning keys
   - Balance data distribution
   - Monitor node health
   - Implement proper error handling

3. **Data Management**
   - Regular backups
   - Data validation
   - Access control
   - Performance monitoring
