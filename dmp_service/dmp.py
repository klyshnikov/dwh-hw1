import psycopg2
from kafka import KafkaConsumer
import json
import threading
from datetime import datetime

def dmp_aircraft():

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
        
def dmp_airports():

    consumer = KafkaConsumer(
        "postgres.public.airports",
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
                h2 = row["airport_code"]
                h3 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                h4 = 'kafka'
                h1 = str(hash(h2) + hash(h3) + hash(h4))
            	
                s1 = h1
                s2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                s3 = ""
                s4 = "kafka"
                s5 = row["airport_code"]
                s6 = row["airport_name"]
                s7 = row["city"]
                s8 = row["coordinates_lon"]
                s9 = row["coordinates_lat"]
                s10 = row["timezone"]
            	
                sql_hub = """
    				INSERT INTO hub_airport (hub_airport_key, hub_airport_bk, hub_load_dts, hub_rec_src)
    				VALUES (%s, %s, %s, %s)
				"""
				
                cursor.execute(sql_hub, (h1, h2, h3, h4))
            	
                sql_sat = """
            		INSERT INTO sat_airport (hub_airport_key, sat_load_dts, hash_diff, sat_rec_src, airport_code, airport_name, city, coordinates_lon, coordinates_lat, timezone)
            		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            	"""
                cursor.execute(sql_sat, (s1, s2, s3, s4, s5, s6, s7, s8, s9, s10))
                
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
        
def dmp_seats():

    consumer = KafkaConsumer(
        "postgres.public.seats",
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
                h2 = row["seat_no"]
                h3 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                h4 = 'kafka'
                h1 = str(hash(h2) + hash(h3) + hash(h4))
            	
                s1 = h1
                s2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                s3 = ""
                s4 = "kafka"
                s5 = row["seat_no"]
                s6 = row["fare_conditions"]
                
                l2 = h1
                l3 = 1
                l4 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                l5 = "kafka"
                l1 = str(hash(l2) + hash(l3) + hash(l4) + hash(l5))
            	
                sql_hub = """
    				INSERT INTO hub_seat (hub_seat_key, hub_seat_bk, hub_load_dts, hub_rec_src)
    				VALUES (%s, %s, %s, %s)
				"""
				
                cursor.execute(sql_hub, (h1, h2, h3, h4))
            	
                sql_sat = """
            		INSERT INTO sat_seat (hub_seat_key, sat_load_dts, hash_diff, sat_rec_src, seat_no, fare_condition)
            		VALUES (%s, %s, %s, %s, %s, %s)
            	"""
                cursor.execute(sql_sat, (s1, s2, s3, s4, s5, s6))
                
                sql_lnk = """
                    INSERT INTO lnk_seat_on_aircraft (lnk_seat_on_aircraft, hub_seat_key, hub_aircraft_key, lnk_load_dts, lnk_rec_src)
                    VALUES (%s, %s, SELECT h.hub_aircraft_key FROM hub_aircraft as h WHERE h.hub_aircraft_bk = %s, %s, %s)
                """
                
                cursor.execute(sql_lnk, (l1, l2, l3, l4, l5))
                
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

def main():
    threads = []
    
    dmp_aircraft_thread = threading.Thread(target=dmp_aircraft)
    threads.append(dmp_aircraft_thread)
    dmp_aircraft_thread.start()
    
    dmp_airports_thread = threading.Thread(target=dmp_airports)
    threads.append(dmp_airports_thread)
    dmp_airports_thread.start()
    
    dmp_seats_thread = threading.Thread(target=dmp_seats)
    threads.append(dmp_seats_thread)
    dmp_seats_thread.start()

main()
