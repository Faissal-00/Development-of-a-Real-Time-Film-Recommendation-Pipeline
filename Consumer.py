from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StringType, ArrayType, FloatType, IntegerType

# Initialize Spark session with necessary packages
spark = SparkSession.builder\
    .appName("KafkaConsumer")\
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.4,"
            "com.datastax.spark:spark-cassandra-connector_2.12:3.2.0") \
    .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true") \
    .getOrCreate()

# Kafka configuration
kafka_bootstrap_servers = 'localhost:9092'  # Adjust the Kafka broker address as needed
kafka_topic = 'movies'

# Define the schema for the incoming JSON messages
schema = StructType() \
    .add("genre_ids", ArrayType(IntegerType())) \
    .add("popularity", FloatType()) \
    .add("title", StringType())

# Read messages from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .load()

# Convert the value column to string and parse JSON data according to the defined schema
parsed_df = df \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema).alias("data")) \
    .select("data.*")

# Output the consumed data to the console
query = parsed_df \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()