import psycopg2
from kafka import KafkaConsumer
import json

def main():

    consumer = KafkaConsumer(
        "postgres.public.aircafts",
        bootstrap_servers=["broker1:29092"],
        group_id="dmp-group",
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: x.decode('utf-8')
    )

    pg_connector = psycopg2.connect(
        host="postgres_dwh",
        port=5432,
        database="postgres",
        user="postgres",
        password="postgres"
    )
    
    cursor = pg_connector.cursor()

    print("consumer and postgres connector was created")

    try:
        for message in consumer:
            message_value = message.value
            print(f"message value: {message_value}")
            
            message_insert_values = json.loads(message_value)["payload"]["after"]
            print(f"insert values: {message_insert_values}")

            try:
                cursor.execute(
                    "INSERT INTO test (id) VALUES (1)"
                )
                pg_connector.commit()
            except Exception as e:
                print(f"Database error: {e}")
                pg_connector.rollback()
    except Exception as e:
            print("Closing consumer due to error\n")
            print(e)
    finally:
        consumer.close()
        cursor.close()
        pg_connector.close()

main()
