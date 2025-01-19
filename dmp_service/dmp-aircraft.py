import psycopg2
from kafka import KafkaConsumer
import json
from datetime import datetime

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
            
            row = json.loads(message_value)["payload"]["after"]
            print(f"insert values: {row}")

            try:
                h2 = row["aircraft_code"]
                h3 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                h4 = 'kafka'
                h1 = str(hash(h2) + hash(h3) + hash(h4))
            	
                s1 = h1
                s2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                s3 = ""
                s4 = "kafka"
                s5 = row["aircraft_code"]
                s6 = row["model"]
                s7 = row["range"]
            	
                sql_hub = """
    				INSERT INTO hub_aircraft (hub_aircraft_key, hub_aircraft_bk, hub_load_dts, hub_rec_src)
    				VALUES (%s, %s, %s, %s)
				"""
				
                cursor.execute(sql_hub, (h1, h2, h3, h4))
            	
                sql_sat = """
            		INSERT INTO sat_aircraft (hub_aircraft_key, sat_load_dts, hash_diff, sat_rec_src, aircraft_code, model, range)
            		VALUES (%s, %s, %s, %s, %s, %s, %s)
            	"""
                cursor.execute(sql_sat, (s1, s2, s3, s4, s5, s6, s7))
                
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
