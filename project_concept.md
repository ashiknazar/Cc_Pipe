## Project Concept
- You’ll build a real-time data pipeline that continuously fetches live cryptocurrency price data from the CoinCap WebSocket API, processes it using PySpark Structured Streaming, and outputs analytics like:
  - top price changes,
  - average price trends,
  - volatility metrics.
- This simulates a real-world financial streaming system, where incoming data never stops.
____
### 1. Data Source: CoinCap API

#### API Endpoint
- WebSocket endpoint:
```bash
wss://ws.coincap.io/prices?assets=bitcoin,ethereum,cardano,solana,dogecoin
```
- This provides continuous live updates in JSON format, e.g.:

```bash
{
  "bitcoin": "68340.12",
  "ethereum": "3721.05",
  "cardano": "0.509",
  "solana": "182.45"
}

```
___
### 2. System Architecture
- conceptual flow
```bash
CoinCap WebSocket → Kafka (message broker) → Spark Structured Streaming → HDFS / Dashboard
```
| Layer                     | Tool                          | Purpose                                         |
| ------------------------- | ----------------------------- | ----------------------------------------------- |
| **Data Source**           | CoinCap WebSocket             | Streams live crypto prices                      |
| **Ingestion**             | Kafka (Producer)              | Receives JSON data and distributes to consumers |
| **Processing**            | PySpark Structured Streaming  | Aggregates, filters, computes metrics           |
| **Storage/Visualization** | HDFS / PostgreSQL / Streamlit | Persist or visualize results                    |
___
### 3.Data Model (per event)

| Field       | Type     | Description                 |
| ----------- | -------- | --------------------------- |
| `timestamp` | `string` | UTC timestamp when received |
| `asset`     | `string` | e.g. "bitcoin"              |
| `price_usd` | `float`  | Current price in USD        |

___
### 4.Example analytic to compute
| Metric                      | Description                        | Example Output    |
| --------------------------- | ---------------------------------- | ----------------- |
| **Current Price Table**     | Latest prices per coin             | bitcoin: $68,300  |
| **Rolling Average (1 min)** | Average price over 1-minute window | ethereum: $3,710  |
| **Volatility**              | Std deviation over last N seconds  | dogecoin: ±0.5%   |
| **Change Alert**            | Detect >2% change in last 10 sec   | Trigger alert log |

___
### 5.tools used
| Component        | Tool                             | Why                                |
| ---------------- | -------------------------------- | ---------------------------------- |
| Stream Source    | **CoinCap API**                  | Real-time, free, no key            |
| Broker           | **Apache Kafka**                 | Most popular for message streaming |
| Processing       | **PySpark Structured Streaming** | Scalable analytics in Python       |
| Visualization    | **Streamlit** or **Grafana**     | Real-time dashboard                |
| Optional Storage | **HDFS / Parquet / PostgreSQL**  | Save processed data                |

___
### 6.Learning Outcomes

- By completing this, you’ll gain hands-on experience with:
  - Real-time WebSocket streaming
  - Kafka producer/consumer flow
  - PySpark Structured Streaming
  - Windowed aggregations & metrics
  - (Optional) Building live dashboards
___

### 7. Extensions (Optional Future Enhancements)
- Once you have the base pipeline running, you can:
  - Add multiple assets dynamically from the API.
  - Introduce machine learning models (e.g., anomaly detection for price jumps).
  - Store aggregates in a NoSQL DB (e.g., Cassandra, MongoDB).
  - Use Airflow for scheduling batch jobs.
  - Deploy the system on Docker or AWS EMR.
___
### 8.Practical Setup Phases

- We can structure your implementation in 5 guided steps:

| Phase                         | Description                                            |
| ----------------------------- | ------------------------------------------------------ |
| **1️⃣ Setup**                 | Install & verify Kafka + Spark on Ubuntu               |
| **2️⃣ Ingestion**             | Connect to CoinCap WebSocket → produce Kafka stream    |
| **3️⃣ Processing**            | Use PySpark Structured Streaming to process live data  |
| **4️⃣ Storage/Visualization** | Write to console, file, or Streamlit dashboard         |
| **5️⃣ Optimization**          | Add windowed aggregations, rolling averages, or alerts |
