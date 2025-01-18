import psycopg2
from kafka import KafkaConsumer
import os
import json

# Kafka Consumer Configuration
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "broker1:29092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "postgres.public.aircafts")
KAFKA_GROUP = os.getenv("KAFKA_GROUP", "dmp-group")

# PostgreSQL Configuration
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres_dwh")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

def main():
    # Set up Kafka Consumer
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        group_id=KAFKA_GROUP,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: x.decode('utf-8')
    )

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    cursor = conn.cursor()

    print("DMP service is running...")

    try:
        for message in consumer:
            # Parse message
            message_value = message.value
            print(f"Received message: {message_value}")

            # Insert message into PostgreSQL
            try:
                cursor.execute(
                    "INSERT INTO test (id) VALUES (1)"
                )
                conn.commit()
                print("Message saved to database.")
            except Exception as e:
                print(f"Database error: {e}")
                conn.rollback()
    except KeyboardInterrupt:
        print("Shutting down DMP service...")
    finally:
        consumer.close()
        cursor.close()
        conn.close()

main()
