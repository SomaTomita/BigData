# NoSQL Database Overview

## Traditional Relational Databases vs NoSQL

### What is a Relational Database?

Traditional databases were based on the 'relational model'. In this model:

- Databases are structured as a collection of tables
- Each row represents a record about a specific entity
- Columns represent attributes of those entities
- Each entity is defined by its set of attributes

### The Emergence of NoSQL

NoSQL databases have gained attention since the early 21st century as new database technologies not based on the relational model. They are also known as "Not only SQL," indicating that they offer more flexible data management beyond traditional SQL.

## Why NoSQL is Gaining Popularity

### 1. Enhanced Scalability

- **Vertical Scaling (Traditional)**:

  - Adding more memory
  - Upgrading to faster CPUs
  - Has physical limitations

- **Horizontal Scaling (NoSQL)**:
  - Distributes workload across multiple servers
  - Easy scale-up by adding more servers

### 2. Flexible Data Structures

- Easy handling of unstructured data
- Supports various data formats such as:
  - Documents
  - Graphs
  - Key-value pairs

## Database Management System (DBMS) Hierarchy

### Three Important Views

1. Physical View
2. Logical View
3. User View

## Data Consistency Models: ACID vs BASE

### ACID Model

Designed for robust transaction processing

1. **Atomic**

   - Transactions either completely succeed or completely fail
   - No partial execution allowed

2. **Consistent**

   - All users see the same updated data after transaction completion

3. **Isolated**

   - Transactions don't interfere with each other
   - Appears to execute in sequence

4. **Durable**
   - Transaction results are permanent
   - Preserved even in case of system failures

### BASE Model

A flexible model adopted by NoSQL databases

1. **Basic Availability**

   - System is basically available most of the time

2. **Soft-state**

   - Temporary inconsistencies are allowed after updates

3. **Eventually consistent**
   - System will eventually reach a consistent state

## Main Types of NoSQL Databases

### 1. Key-Value Databases

- The simplest form of NoSQL
- Data stored as key-value pairs
- Values can be any data type (text, images, etc.)
- Known for fast data access

### 2. Document Databases

- An evolution of key-value stores
- Stores data in structured document formats
- Common formats include:
  - XML
  - JSON
  - BSON (Binary JSON)
- Enables more complex queries and searches

### 3. Graph Databases

- Uses concepts of nodes, edges, and properties
- Capable of representing complex relationships
- Key features:
  - Nodes: Represent data points
  - Edges: Represent relationships between nodes
  - Properties: Define node attributes
- Ideal for hierarchical or network-structured data

## Summary

NoSQL databases are flexible database solutions developed to handle the modern big data era. Compared to traditional relational databases, they offer more flexible scaling and support for diverse data structures. However, it's crucial to select the appropriate type of NoSQL database based on your specific use case.
