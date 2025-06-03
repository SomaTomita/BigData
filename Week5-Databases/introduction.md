# Chapter 1 – Foundations of Database Management

## Learning Goals

- **Differentiate file-based vs database approach**  
  Example: Sober startup considering Word/Excel vs relational DB.
- **Recognize key components of a database system** (data, software, users, hardware).
- **List tangible benefits of DBMS** (reduced redundancy, concurrency control, scalability).

## 1. Opening Scenario – The Sober Startup

Sober is evaluating how to store customer, order, and product data. Saving everything in Word docs and Excel sheets might feel familiar, but it recreates the 1960s file‑based era. The chapter uses Sober’s dilemma to motivate modern DBMS adoption.  
**Concrete illustration:** imagine Sober’s sales team editing `customers.xlsx` while the finance team keeps a separate `invoice.docx`. The moment a client changes address only finance knows about, Sober ships to the wrong place.

## 1.1 Applications of Database Technology

| Domain                 | Typical Data                      | Example System               |
| ---------------------- | --------------------------------- | ---------------------------- |
| Inventory control      | SKU, stock level, reorder point   | Amazon fulfilment centre     |
| Multimedia libraries   | Audio/video metadata, thumbnails  | Spotify, Netflix             |
| Biometrics             | Fingerprint hash, retina scan     | ePassport gates at airports  |
| Wearables / IoT        | Heart rate, GPS, accelerometer    | Apple Watch health dashboard |
| Geospatial (GIS)       | Lat/long, road network, zoning    | Google Maps, Waze            |
| High‑frequency trading | Price ticks, order book snapshots | Goldman Sachs trading engine |
| Industrial sensors     | Reactor temperature, pressure     | Nuclear plant SCADA          |
| Retail Big Data        | POS transactions, loyalty IDs     | Walmart’s Teradata warehouse |

These examples show that a _database_ can hold numbers, text, images, sound, or streams arriving thousands of times per second.

## 1.2 Key Definitions

### Database

A **database** is an organised collection of related data describing a business process.  
**Example:** In a purchase‑order database:

- **Product** ⇢ `ProductID`, `Name`, `Colour`
- **Supplier** ⇢ `SupplierID`, `Name`, `Address`
- **PurchaseOrder** ⇢ `PONumber`, `PODate`

Relationships connect these entities (each `Product` can have many `Suppliers`; each `PurchaseOrder` references one `Supplier`).

### Database Management System (DBMS)

Software that **defines**, **creates**, **uses**, and **maintains** the database. Core modules include:

1. **Data definition** – interprets `CREATE TABLE …`.
2. **Query processor** – optimises and runs `SELECT …`.
3. **Storage manager** – organises files, handles crashes.
4. **Transaction & concurrency** – ACID guarantees.

Commercial examples: Oracle, Microsoft SQL Server, IBM Db2. Open‑source: MySQL, PostgreSQL.

### Database System

The union of the DBMS _and_ the database itself, plus associated users, apps, and hardware.

## 1.3 File‑Based versus Database Approach

### 1.3.1 The File‑Based Approach

| Application | Private File & Fields                    |
| ----------- | ---------------------------------------- |
| Invoicing   | `CustomerNr`, `CustomerName`, `VATCode`  |
| CRM         | `CustomerNr`, `CustomerName`, `Turnover` |
| GIS         | `CustomerNr`, `CustomerName`, `ZipCode`  |

Because each program owns its file, **duplicate data** proliferates. Problems follow:

1. **Redundancy & wasted storage**  
   Same customer stored three times. With 1 M clients and 50 B of duplicated bytes, backups balloon and cloud bills rise.

2. **Update anomalies (inconsistency)**  
   Marketing corrects `CustomerName = "ACME Corp"` in the CRM file, but GIS still shows `ACME Incorporated`, causing mismatched labels in a mail‑merge.

3. **Structural inflexibility (tight coupling)**  
   Adding a `PhoneNumber` column means patching _every_ program that parses the file structure.

4. **Poor concurrency control**  
   No central transaction log. If Accounts edits `VATCode` while Sales recalculates turnover, race conditions can leave hybrid records.

5. **Integration road‑blocks**  
   Building a self‑service web portal that shows invoices and delivery maps would require messy ETL scripts to reconcile three incompatible formats.

> **Real‑world case:** A mid‑sized hospital once stored patient data in 250+ departmental spreadsheets. During a flu outbreak, divergent spellings of patient names led to double‑dosing of vaccines. A central DBMS later eliminated >90 % of such incidents.

---

## Why the Database Approach Wins (Preview)

- **Single source of truth** eliminates redundancy.
- **ACID transactions** guarantee consistency even with 1,000 concurrent users.
- **Data independence** allows schemas to evolve without rewriting every application.
- **Security & auditing** are centralised (roles, row‑level policies, logs).  
  We explore these benefits and the architecture of a DBMS in Chapter 2.

---

### Retention Check

1. List two multimedia and two IoT examples where a DBMS is essential.
2. Define _database_, _DBMS_, and _database system_ in your own words.
3. Explain how a change in file structure can break a legacy COBOL program.

---

_Prepared for Sober startup – feel free to iterate or append additional pages._

## 1.3.2 The Database Approach – Centralising the Truth

Under the **database approach**, every application (Invoicing, CRM, GIS ...) no longer opens its
own flat file. Instead, it speaks to a _single_ DBMS instance that stores:

| Layer                  | Contents                                                  |
| ---------------------- | --------------------------------------------------------- |
| **Raw data**           | Customer tuples, invoice rows, spatial coordinates ...    |
| **Metadata (catalog)** | Table definitions, indexes, constraints, view definitions |

### Why it is Superior

1. **No duplication – one table, one customer.**
2. **Consistency by design – ACID transactions** keep data correct under concurrency.
3. **Data independence** – applications need not change when storage structures evolve.
4. **Declarative querying** – replace 30‑line file scans with a one‑line SQL statement.

**Pseudo‑code vs SQL illustration**

```pseudo
# File approach
open Customer.txt
while not EOF:
    if name == 'Bart':
        print record
```

```sql
-- Database approach
SELECT *
FROM   Customer
WHERE  name = 'Bart';
```

The DBMS planner decides whether to use an index, parallel scan, or in‑memory cache—completely
transparent to the developer.

---

## 1.4 Elements of a Database System

### 1.4.1 Database Model vs Instances

_Model (schema)_ = blueprint.  
_Instance (state)_ = current data snapshot.

```text
Student  (number, name, address, email)
Course   (number, name)
Building (number, address)
```

### 1.4.2 Data Models – Different Lenses on the Same Reality

| Perspective         | Purpose                                               | Typical Notation        |
| ------------------- | ----------------------------------------------------- | ----------------------- |
| **Conceptual**      | Talk to business users; ignore implementation details | EER diagram             |
| **Logical**         | Map to a technology (relational, XML, NoSQL)          | Relational schema, XSD  |
| **Internal**        | Describe physical storage                             | Heap file, B‑tree index |
| **External / View** | Provide tailored subsets for apps or roles            | SQL views               |

### 1.4.3 The Three‑Layer Architecture

**Logical data independence**  
⇢ You can split `CustomerName` into `FirstName` / `LastName` at the logical layer without touching
`finance_view` or `logistics_view`.

**Physical data independence**  
⇢ DBAs may move hot partitions from London to a faster SSD array in Washington; applications are
unaware.

### 1.4.4 The Catalog – The DBMS Brain

The catalog (data dictionary) tracks:

- All table and column definitions
- Primary & foreign keys, constraints
- User permissions and roles
- Statistics for the optimiser

Because every tool (loader, query engine, backup) consults the same catalog, **metadata
consistency** is guaranteed.

### 1.4.5 Database Users – Who Does What?

| Role                      | Key Responsibility                                           |
| ------------------------- | ------------------------------------------------------------ |
| **Information architect** | Captures business requirements, builds conceptual model      |
| **Database designer**     | Translates to logical & internal models                      |
| **DBA**                   | Installs DBMS, tunes performance, manages security & backups |
| **Application developer** | Writes business logic (Java, Python) that consumes data      |
| **Business user**         | Runs reports, enters orders, explores ad‑hoc queries         |

---

### Quick Self‑Check

1. Explain two forms of _data independence_ and why they matter.
2. Which user role would create a new _view_ for the Marketing department?
3. Give an example where logical and physical changes happen simultaneously.

## 1.4.6 Database Languages

Every modern DBMS ships with **two primary language families**:

| Purpose                              | Language                               | Typical Keywords              | Primary User |
| ------------------------------------ | -------------------------------------- | ----------------------------- | ------------ |
| **Data Definition Language (DDL)**   | `CREATE`, `ALTER`, `DROP`, `TRUNCATE`  | DBA / Database Designer       |
| **Data Manipulation Language (DML)** | `SELECT`, `INSERT`, `UPDATE`, `DELETE` | App Developer / Business User |

> **Example – creating & using a table in SQL (both DDL & DML)**
>
> ```sql
> -- DDL: define a table
> CREATE TABLE Student (
>   number   CHAR(8)  PRIMARY KEY,
>   name     VARCHAR(50),
>   address  VARCHAR(100),
>   email    VARCHAR(100)
> );
>
> -- DML: manipulate data
> INSERT INTO Student VALUES ('0158554', 'Bart Baesens',
>                             '1040 Market Street, SF',
>                             'Bart.Baesens@kuleuven.be');
>
> SELECT name, email
> FROM   Student
> WHERE  number = '0158554';
> ```
>
> The definitions are stored in the **catalog**, while queries/updates can be embedded in Java, Python, or executed interactively from a GUI.

---

## 1.5 Advantages of Database Systems & Database Management

### 1.5.1 Data Independence

- **Physical Data Independence**  
  Changes in storage (new indexes, SSD migration, sharding) do **not** require application rewrites.
- **Logical Data Independence**  
  Schema evolution (add `PhoneNumber`, split `Name`) leaves external views & programs largely untouched.

Both forms rely on the _interfaces_ between the three layers to absorb change gracefully.

### 1.5.2 Database Modeling

A rigorous **data model** ensures a single, shared understanding of:

- entities & relationships
- business rules (integrity constraints)
- assumptions & known gaps

Well‑defined models (ER, relational, object‑oriented ...) shorten development time and improve data quality.

### 1.5.3 Managing Structured, Semi‑Structured & Unstructured Data

| Data Type           | Example                        | Suitable Technology           |
| ------------------- | ------------------------------ | ----------------------------- |
| **Structured**      | `Student(number, name, email)` | Relational DB, columnar store |
| **Semi‑Structured** | HTML résumé, JSON tweet        | XML DB, NoSQL document store  |
| **Unstructured**    | PDF contract, JPEG photo       | Object store, search engine   |

Modern DBMSs blend full‑text search, image metadata, and JSON handling into a single platform.

### 1.5.4 Managing Data Redundancy

Controlled duplication (replication, caching) **improves read latency** yet remains _consistent_ through DBMS‑managed synchronisation—unlike uncontrolled copies in siloed files.

### 1.5.5 Specifying Integrity Rules

- **Syntactic** — `customerID INT NOT NULL`, `birthDate DATE`
- **Semantic** — `CHECK (balance >= 0)`, `UNIQUE(email)`

Centralising rules in the catalog eliminates duplicated validation code and prevents anomalies.

### 1.5.6 Concurrency Control & ACID

A **transaction** behaves atomically and respects the **ACID** properties:

| Property        | Meaning                                 |
| --------------- | --------------------------------------- |
| **Atomicity**   | All or nothing                          |
| **Consistency** | Move DB from one valid state to another |
| **Isolation**   | Concurrent transactions appear serial   |
| **Durability**  | Committed changes survive crashes       |

Lost‑update, dirty‑read, and other hazards are mitigated by locks, MVCC, or timestamp ordering.

### 1.5.7 Backup & Recovery

- **Full / incremental backups** automate disaster preparedness.
- **Point‑in‑time recovery** replays the write‑ahead log to any second before failure.

### 1.5.8 Data Security

Role‑based privileges (`GRANT SELECT ON Invoice TO auditor`) safeguard sensitive information. Credentials and policies live in—again—the catalog.

### 1.5.9 Performance Utilities

Key Performance Indicators (KPIs):

1. **Response Time** – latency per request
2. **Throughput** – transactions/sec
3. **Space Utilisation** – bytes for data + metadata

DBAs employ partitioning, indexing, query plan caching and buffer tuning to keep KPIs healthy.

---

### Retention Questions

1. _List the main components of a database system and describe their roles._
2. _Using the three‑layer architecture, explain where logical data independence applies._
3. _Define the catalog and outline two reasons it is critical._
4. _Why are ACID properties essential for online banking?_
5. _Give an example of structured vs semi‑structured vs unstructured data in a social‑media app._

---

## Chapter Summary

- File‑based silos were replaced by **centralised DBMSs** offering shared storage and rich query languages.
- The **three‑layer architecture** (external · logical · internal) provides data independence.
- A spectrum of **data models** enables precise representation, from conceptual EER to physical pages.
- DBMSs deliver **integrity, security, concurrency, backup, and performance** out‑of‑the‑box—freeing developers to focus on business value.

---

## Key Terms

`ACID`, `catalog`, `conceptual data model`, `DDL`, `DML`, `data independence`,  
`database`, `database approach`, `DBMS`, `database state`, `external view`,  
`file‑based approach`, `internal data model`, `logical data independence`,  
`metadata`, `semi‑structured data`, `three‑layer architecture`, `unstructured data`, `view`

---

# Reading Questions and Answers

**Question: What are the key problems with the file-based approach to data management, and how does a DBMS address them?**

The file-based approach to data management faces several critical challenges that significantly impact business operations and data integrity. In this approach, each application maintains its own separate files, leading to data redundancy where the same information is stored multiple times across different files. For instance, as illustrated in the chapter, customer information might be duplicated across invoicing, CRM, and GIS systems. This redundancy not only wastes storage space but also creates update anomalies where data modifications in one file may not be reflected in others, leading to inconsistencies. The file-based system also suffers from poor concurrency control, making it difficult to manage multiple users accessing data simultaneously, and lacks structural flexibility, requiring extensive program modifications when file structures change.

A Database Management System (DBMS) addresses these issues through several mechanisms. It provides a centralized approach where data is stored once and accessed by multiple applications, eliminating redundancy. The DBMS ensures data consistency through ACID transactions, maintains data independence allowing structural changes without affecting applications, and implements robust concurrency control mechanisms. Additionally, it offers centralized security and auditing capabilities, making data management more secure and trackable.

**Question: Why is it important to clearly define data and metadata in the context of a database system?**

Clearly defining data and metadata is crucial in a database system as it forms the foundation for effective data management and system operation. Data represents the actual information stored in the database, while metadata (stored in the catalog or data dictionary) describes the structure, relationships, and constraints of that data. This clear definition is essential because it enables the DBMS to maintain data integrity, optimize query processing, and ensure proper data access control.

The catalog, serving as the DBMS's brain, maintains all table and column definitions, primary and foreign keys, constraints, user permissions, and optimization statistics. This centralized metadata management ensures consistency across all database operations, from data loading to query processing and backup procedures. Furthermore, well-defined metadata supports the three-layer architecture (external, logical, and internal), enabling both logical and physical data independence, which are crucial for system flexibility and maintenance. Without clear metadata definitions, it would be impossible to implement features like views for different user groups or enforce data integrity constraints effectively.
