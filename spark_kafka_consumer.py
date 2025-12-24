from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, DoubleType

spark = (
    SparkSession.builder
    .appName("KafkaToHDFS")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

schema = StructType() \
    .add("asset", StringType()) \
    .add("price_usd", DoubleType()) \
    .add("event_time", StringType())

df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "crypto_prices")
    .option("startingOffsets", "latest")
    .load()
)

parsed = (
    df.selectExpr("CAST(value AS STRING) AS json")
      .select(from_json(col("json"), schema).alias("data"))
      .select("data.*")
)

# Console output (debug)
console_query = (
    parsed.writeStream
    .format("console")
    .outputMode("append")
    .option("truncate", False)
    .start()
)

# HDFS output (correct port 8020)
hdfs_query = (
    parsed.writeStream
    .format("parquet")
    .option("path", "hdfs://localhost:8020/crypto/prices")
    .option("checkpointLocation", "hdfs://localhost:8020/crypto/checkpoints")
    .outputMode("append")
    .start()
)

spark.streams.awaitAnyTermination()
