### Table 1: Alert Rules and Conditions

| Rule ID | SQL-level Condition                                               | Business meaning       | Target latency |
| ------- | ----------------------------------------------------------------- | ---------------------- | -------------- |
| A1      | city='London' AND renovation='Designer' AND status='vacant' > 500 | "Luxury vacancy surge" | < 1 s          |
| A2      | AVG(price_usd_month) drops 20 % within 24 h per city              | "Rapid price anomaly"  | < 30 s         |

### Table 2: System Architecture Tiers

| Tier              | Technology                     | Rationale & Requirement Fit                                                                            |
| ----------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------ |
| Ingest / Queue    | Kafka 3-node cluster           | Append-only "event log" for apartment_events; at-least-once delivery; proven >4 trn events day-1 [17]. |
| Stream Compute    | Apache Flink on Kubernetes     | Windowed SQL handles A1/A2 in-memory with <100 ms end-to-end; exactly-once state via RocksDB [18].     |
| Operational Store | PostgreSQL 15 + Citus          | Retains 3 NF schema; shard by apartment_id; strong ACID for transactions.                              |
| Analytical Lake   | Delta Lake on S3 + Spark       | Nightly ETL -> star schema; cheap storage; ad-hoc BI over 100 GB+; Spark unified engine [19].          |
| Autoscale / DR    | Kubernetes HPA + Mirrormaker 2 | Scales Flink TaskManagers & Kafka partitions; cross-region replication for fail-over.                  |

### Table 3: Technology Stack Comparison

| Stack                          | Pros                                                      | Key Limitations                                                 |
| ------------------------------ | --------------------------------------------------------- | --------------------------------------------------------------- |
| Kafka + Flink + Citus (chosen) | Open source, sub-second alerts, ACID SQL, vendor-neutral  | Higher ops complexity, requires DevOps skills                   |
| Pulsar + Storm                 | Built-in geo-replication                                  | Smaller community, fewer SQL APIs                               |
| Aurora Global                  | Managed SQL, low replica lag                              | Single-writer, external stream engine still needed              |
| Hadoop (MapReduce)             | Powerful batch ETL, proven for large-scale job processing | Seconds to minutes latency, no stream support, not cloud native |

### Table 4: Technical Challenges and Mitigations

| Challenge               | Mitigation                                                           |
| ----------------------- | -------------------------------------------------------------------- |
| Exactly-once → Postgres | Kafka transactional sink + event_id unique index                     |
| Network cost            | Z-Std compression, regional brokers, async MirrorMaker replication   |
| Ops complexity          | GitOps (Argo CD), Prometheus + Grafana dashboards, Terraform modules |

## Technology Overview

The proposed architecture combines several modern technologies to create a robust real-time data processing system:

### Core System Components

1. **Ingest / Queue (Apache Kafka)**:

   - Acts as the primary data ingestion layer
   - 3-node cluster ensures high availability and fault tolerance
   - Handles massive throughput (>4 trillion events per day)
   - Provides reliable message delivery with at-least-once semantics
   - Enables event replay and fault recovery

2. **Stream Compute (Apache Flink on Kubernetes)**:

   - Real-time stream processing framework
   - Processes data in-memory for sub-100ms latency
   - Provides exactly-once processing guarantees
   - Uses RocksDB for state management
   - Runs on Kubernetes for scalability and container orchestration

3. **Operational Store (PostgreSQL 15 + Citus)**:

   - Distributed SQL database for real-time operations
   - Maintains ACID compliance while scaling horizontally
   - Shards data by apartment_id for optimal performance
   - Supports complex SQL queries and transactions
   - Ensures data consistency across distributed nodes

4. **Analytical Lake (Delta Lake on S3 + Spark)**:

   - Data lake solution for long-term storage and analytics
   - Provides ACID transactions on top of S3 storage
   - Enables efficient big data processing with Spark
   - Supports schema evolution and time travel features
   - Optimized for large-scale analytical workloads

5. **Autoscale / DR (Kubernetes HPA + Mirrormaker 2)**:
   - Automatic scaling based on workload demands
   - Cross-region replication for disaster recovery
   - Dynamic resource allocation
   - High availability across multiple regions

### Alternative Technologies

**Hadoop (MapReduce) Deep Dive**:

- Traditional batch processing framework
- Advantages:
  - Proven technology for large-scale data processing
  - Excellent for complex ETL jobs
  - Strong data locality
  - Cost-effective for batch analytics
- Limitations:
  - High latency (batch-oriented)
  - Not designed for stream processing
  - Complex deployment in cloud environments
  - Limited real-time capabilities

The architecture prioritizes real-time processing capabilities while maintaining data consistency and fault tolerance. The chosen stack balances performance requirements (sub-second latency for critical alerts) with operational considerations (scalability, maintainability, and disaster recovery).
