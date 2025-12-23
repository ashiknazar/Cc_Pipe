from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Spark session
spark = (
    SparkSession.builder
    .appName("CryptoKafkaConsumerHDFS")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# Kafka source
kafka_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "crypto_prices")
    .option("startingOffsets", "latest")
    .load()
)

# Schema for JSON value
schema = StructType([
    StructField("asset", StringType(), True),
    StructField("price_usd", DoubleType(), True),
    StructField("event_time", StringType(), True)
])

# Parse Kafka value
parsed_df = (
    kafka_df
    .selectExpr("CAST(value AS STRING)")
    .select(from_json(col("value"), schema).alias("data"))
    .select("data.*")
)

# Write stream to HDFS in Parquet format
query = (
    parsed_df
    .writeStream
    .outputMode("append")
    .format("parquet")  # Parquet format
    .option("path", "/home/ashik/codes/Cc_pipe/data/crypto_prices_parquet")
    .option("checkpointLocation", "/home/ashik/codes/Cc_pipe/data/crypto_prices_checkpoint")
    .start()
)

query.awaitTermination()
