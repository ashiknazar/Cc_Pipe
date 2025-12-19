# Crypto Streaming Big Data Pipeline

## Overview

This project implements an **end-to-end Big Data streaming architecture** using **free and open-source tools**. It simulates a real-world financial data pipeline by continuously ingesting cryptocurrency price data from the **CoinGecko REST API**, streaming it through **Apache Kafka**, processing it with **PySpark Structured Streaming**, storing results in **HDFS**, and optionally visualizing metrics using **Streamlit**.

The project is designed for **learning Big Data fundamentals** without cloud costs or paid APIs and runs locally on **Ubuntu 24.04 LTS**.

---

## Key Objectives

* Understand pull-based vs push-based streaming
* Build a Kafka-backed streaming pipeline
* Perform real-time analytics using Spark Structured Streaming
* Store streaming outputs in HDFS using columnar formats
* Gain practical exposure to industry-standard Big Data tools

---

## Architecture (Logical)

```
CoinGecko REST API
        ↓  (poll every N seconds)
Python Producer
        ↓
Apache Kafka (ZooKeeper mode)
        ↓
Spark Structured Streaming (PySpark)
        ↓
HDFS (Parquet files)
        ↓
Streamlit Dashboard (optional)
```

---

## Technology Stack

| Layer         | Tool                  | Purpose                       |
| ------------- | --------------------- | ----------------------------- |
| Data Source   | CoinGecko API         | Free crypto price data        |
| Ingestion     | Python + kafka-python | Poll API and publish events   |
| Messaging     | Apache Kafka 3.4      | Stream buffering & decoupling |
| Coordination  | ZooKeeper             | Kafka metadata management     |
| Processing    | Spark 3.5 (PySpark)   | Real-time analytics           |
| Storage       | Hadoop HDFS 3.3       | Distributed persistence       |
| Format        | Parquet               | Efficient columnar storage    |
| Visualization | Streamlit (optional)  | Live dashboards               |

---

## Data Model

Each Kafka event represents **one asset price update**:

```json
{
  "asset": "bitcoin",
  "price_usd": 68340.12,
  "event_time": "2025-01-01T10:00:10Z"
}
```

---

## Streaming Strategy

* CoinGecko is **not a streaming API**
* Data is ingested using **scheduled polling** (micro-streaming)
* The producer runs in an **infinite loop**
* Spark processes data using **event-time windows**

This approach mirrors how many real-world financial and IoT systems work.

---

## Analytics Implemented

* Latest price per asset
* 1-minute rolling average price
* Short-window volatility (standard deviation)
* Percentage price change detection

---

## Project Structure

```
cc_pipe/
├── producer/
│   └── coingecko_producer.py
├── spark/
│   └── streaming_job.py
├── hdfs/
│   └── output/
├── dashboard/
│   └── app.py   # optional
├── requirements.txt
└── README.md
```

---

## Environment Constraints (Important)

This project is validated for:

* **Ubuntu 24.04 LTS**
* **Java 11 (required)**
* **Python 3.10 (virtual environment)**

Using newer Java (17/21) or system Python (3.12) will cause failures in Hadoop/Spark.

---

## Prerequisites

* Java 11
* Python 3.10 (venv)
* Apache Kafka 3.4 (ZooKeeper mode)
* Apache Hadoop 3.3 (pseudo-distributed)
* Apache Spark 3.5 (Hadoop 3 build)

---

## How to Run (High-Level)

1. Start ZooKeeper
2. Start Kafka broker
3. Create Kafka topic `crypto_prices`
4. Start HDFS (NameNode & DataNode)
5. Run Python producer
6. Submit Spark streaming job
7. (Optional) Run Streamlit dashboard

Detailed commands are documented step-by-step in subsequent setup guides.

---

## Learning Outcomes

By completing this project, you will gain hands-on experience with:

* Kafka-based streaming pipelines
* Spark Structured Streaming internals
* Event-time windowing & aggregations
* HDFS storage and Parquet formats
* Real-world Big Data architectural patterns

---

## Future Enhancements

* Dockerize the entire pipeline
* Add schema registry (Avro/JSON Schema)
* Introduce anomaly detection models
* Add alerting via logs or notifications
* Deploy on cloud-managed services

---

## Disclaimer

This project is for **educational purposes** and uses public market data. It is not intended for trading or financial decision-making.
