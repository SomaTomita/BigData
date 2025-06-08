# Week 5 Summary Quiz - Relational Database Concepts

## Question 1: Key Types (1pt)

**Question:** A **\_\_\_\_** key is a minimal set of attributes that can uniquely identify an entity instance.

**Answer:** candidate

**Detailed Explanation:**

- A candidate key is a minimal set of attributes that uniquely identifies each record in a table
- Key characteristics:
  1. Uniqueness: No two records can have the same value for the candidate key
  2. Minimality: No subset of the attributes can provide unique identification
- Comparison with other key types:
  - Foreign key: References primary key in another table (for relationships)
  - Surrogate key: Artificial identifier (like auto-increment ID)
  - Primary key: The chosen candidate key that will be used as the main identifier
- Example: In a Student table, both StudentID and Email could be candidate keys
  - Both uniquely identify a student
  - Neither can be reduced further (minimal)

## Question 2: ERD Concepts (1pt)

**Question:** Match each ERD concept to its correct description

**Answer:**

- Derived attribute → An attribute calculated from other attributes
- Composite attribute → An attribute formed by combining several sub-parts
- Key attribute → An attribute used to uniquely identify an entity
- Multi-valued attribute → An attribute that stores multiple values

**Detailed Explanation:**

1. Derived Attribute:

   - Calculated from other attributes
   - Not physically stored in database
   - Examples:
     - Age (calculated from DateOfBirth)
     - Total Price (calculated from Quantity × Unit Price)
     - BMI (calculated from Height and Weight)

2. Composite Attribute:

   - Contains multiple component attributes
   - Can be divided into smaller subparts
   - Examples:
     - Address (Street, City, State, ZIP)
     - Full Name (First Name, Middle Name, Last Name)
     - Contact Info (Phone, Email, Address)

3. Key Attribute:

   - Uniquely identifies each entity instance
   - Must be unique and not null
   - Examples:
     - Student ID in a university database
     - Social Security Number
     - Product SKU

4. Multi-valued Attribute:
   - Can hold multiple values simultaneously
   - Usually normalized in actual database implementation
   - Examples:
     - Phone Numbers (home, work, mobile)
     - Email Addresses
     - Skills of an employee

## Question 3: Domain in Relational Model (1pt)

**Question:** Which of the following best describes a domain in the relational model?

**Answer:** A named set of valid values for an attribute

**Detailed Explanation:**

- A domain defines the set of allowable values that an attribute can take
- Components of a domain definition:
  1. Data type (e.g., INTEGER, VARCHAR, DATE)
  2. Format or pattern (e.g., email format, phone number pattern)
  3. Range of values (e.g., 0-100 for percentage)
  4. Constraints (e.g., NOT NULL, UNIQUE)
- Examples:
  1. Gender_Domain = {'M', 'F', 'Other'}
  2. Age_Domain = {x | x is an integer and 0 ≤ x ≤ 150}
  3. Email_Domain = {text matching email format pattern}
- Benefits:
  - Ensures data consistency
  - Prevents invalid data entry
  - Simplifies data validation
  - Improves data quality

## Question 4: Relational Constraints (1pt)

**Question:** Which of the following are relational constraints?

**Answer:**

- Functional dependencies
- Domain constraints
- Referential integrity constraints

**Detailed Explanation:**

1. Functional Dependencies:

   - Defines how attributes depend on each other
   - Format: X → Y (X determines Y)
   - Examples:
     - StudentID → StudentName
     - (CourseID, Semester) → Instructor
   - Used in normalization process

2. Domain Constraints:

   - Restricts attribute values to defined domains
   - Types:
     - Data type constraints
     - Range constraints
     - Format constraints
     - Custom rules
   - Examples:
     - Age must be positive
     - Email must match valid format
     - Grade must be A, B, C, D, or F

3. Referential Integrity Constraints:
   - Ensures valid references between tables
   - Rules:
     - Foreign key must match existing primary key
     - Foreign key can be NULL (if allowed)
   - Examples:
     - Order.CustomerID must exist in Customer.CustomerID
     - Enrollment.CourseID must exist in Course.CourseID

Note: Hierarchical constraints are not relational database constraints (they belong to hierarchical databases)

## Question 5: Key Concepts (1pt)

**Question:** Match each term with its correct definition.

**Answer:**

- Superkey → A set of one or more attributes that uniquely identifies tuples and may contain extraneous attributes
- Primary Key → A selected candidate key used to uniquely identify tuples in a relation
- Foreign Key → An attribute in one relation that references the primary key in another

**Detailed Explanation:**

1. Superkey:

   - Properties:
     - Ensures uniqueness
     - May contain extra attributes
     - Not necessarily minimal
   - Example:
     - If StudentID is a key, then {StudentID, Name} is a superkey
     - {StudentID, Email, Phone} when StudentID alone is sufficient

2. Primary Key:

   - Properties:
     - Chosen from candidate keys
     - Must be unique
     - Cannot be NULL
     - Should be immutable
   - Selection criteria:
     - Simplicity
     - Stability
     - Familiarity
     - Size (smaller is better)

3. Foreign Key:
   - Properties:
     - Creates relationships between tables
     - Must match primary key in referenced table
     - Can be NULL (if allowed)
   - Examples:
     - OrderDetails.OrderID references Orders.OrderID
     - Employee.DepartmentID references Department.DepartmentID

## Question 6: Primary Key Purpose (1pt)

**Question:** What is the main purpose of a primary key in the relational model?

**Answer:** To uniquely identify each row in a table

**Detailed Explanation:**
Primary keys serve multiple purposes:

1. Unique Identification:

   - Ensures each record can be uniquely identified
   - Prevents duplicate records
   - Enables precise record retrieval

2. Data Integrity:

   - Cannot contain NULL values
   - Must be unique
   - Often used as a reference point for foreign keys

3. Performance:

   - Automatically indexed
   - Optimizes search operations
   - Improves JOIN performance

4. Relationship Management:
   - Enables table relationships
   - Supports referential integrity
   - Facilitates data normalization

## Question 7: Relational Concepts (1pt)

**Question:** Match each relational concept with its description.

**Answer:**

- Entity Integrity → Ensures that the value of a primary key is never null
- Referential Integrity → Ensures foreign keys match existing primary keys or are null
- Domain Constraint → Restricts attribute values to a set of permissible values
- Tuple → A single row in a relation

**Detailed Explanation:**

1. Entity Integrity:

   - Rules:
     - Primary key cannot be NULL
     - Primary key must be unique
   - Purpose:
     - Ensures each entity is uniquely identifiable
     - Maintains data consistency
   - Example:
     - Every student must have a unique StudentID

2. Referential Integrity:

   - Rules:
     - Foreign key must match existing primary key
     - Foreign key can be NULL (if allowed)
   - Actions on parent deletion:
     - CASCADE: Delete child records
     - SET NULL: Set foreign key to NULL
     - RESTRICT: Prevent deletion
   - Example:
     - Cannot add an order for non-existent customer

3. Domain Constraint:

   - Types:
     - Data type constraints
     - Range constraints
     - Pattern constraints
     - Custom rules
   - Examples:
     - Age must be between 0 and 150
     - Email must match valid format
     - Status must be 'Active' or 'Inactive'

4. Tuple:
   - Properties:
     - Represents one complete record
     - Contains values for each attribute
     - Must follow all table constraints
   - Example:
     - One complete student record with all attributes

## Question 8: Partial Dependencies (1pt)

**Question:** A table with a single-column primary key cannot have partial dependencies.

**Answer:** True

**Detailed Explanation:**

- Partial dependencies can only occur with composite primary keys
- Understanding partial dependencies:

  1. Definition:

     - Non-key attribute depends on part of composite key
     - Violates 2NF requirements

  2. Example with composite key:

     - Primary Key: (StudentID, CourseID)
     - StudentName depends only on StudentID
     - This is a partial dependency

  3. Single-column primary key:
     - All non-key attributes must depend on entire key
     - No subset of key exists
     - Therefore, partial dependencies impossible

## Question 9: Unnormalized Table Issues (1pt)

**Question:** Issues in the UNREGISTERED_COURSES table

**Answer:**

- Data redundancy
- Multi-valued attributes

**Detailed Explanation:**

1. Data Redundancy:

   - Same information repeated:
     - Instructor information duplicated
     - Course details repeated
   - Problems caused:
     - Update anomalies
     - Insert anomalies
     - Delete anomalies
     - Storage inefficiency

2. Multi-valued Attributes:
   - Multiple values in single column:
     - CourseCode: "CS101, CS102"
     - CourseName: "Programming, Databases"
     - Instructor: "Dr Smith, Dr Jones"
     - InstructorPhone: "1234567890, 0987654321"
     - Grade: "A, B"
   - Violates 1NF requirements
   - Makes data manipulation difficult

## Question 10: Normalization Steps (1pt)

**Question:** Match the normalization step with the resulting schema transformation.

**Answer:**

- Apply 1NF → Student-Course pairs flattened
- Apply 2NF → Separate Course and Instructor details
- Apply 3NF → Instructor contact details separated

**Detailed Explanation:**

1. First Normal Form (1NF):

   - Actions:
     - Eliminate multi-valued attributes
     - Create separate rows for each value
     - Ensure atomic values
   - Result:
     - One row per student-course combination
     - All attributes contain single values
   - Example transformation:

     ```
     Before:
     StudentID | Courses
     1        | CS101, CS102

     After:
     StudentID | Course
     1        | CS101
     1        | CS102
     ```

2. Second Normal Form (2NF):

   - Actions:
     - Remove partial dependencies
     - Create separate tables for independent entities
   - Result:
     - Course details separated from enrollment
     - Instructor details linked to courses
   - Example tables:
     - Students(StudentID, StudentName)
     - Courses(CourseID, CourseName, Instructor)
     - Enrollments(StudentID, CourseID, Grade)

3. Third Normal Form (3NF):
   - Actions:
     - Remove transitive dependencies
     - Further normalize related data
   - Result:
     - Instructor contact information in separate table
     - No non-key attributes depend on other non-key attributes
   - Final tables:
     - Students(StudentID, StudentName)
     - Courses(CourseID, CourseName, InstructorID)
     - Instructors(InstructorID, Name, Phone)
     - Enrollments(StudentID, CourseID, Grade)
