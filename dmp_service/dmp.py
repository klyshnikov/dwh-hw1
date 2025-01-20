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
                l3 = row["aircraft_code"]
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
                
                pg_connector.commit()
                
                sub_1 = """
                    SELECT h.hub_aircraft_key FROM hub_aircraft as h WHERE h.hub_aircraft_bk = %s
                """
                
                cursor.execute(sub_1, (l3))
                
                result = cursor.fetchone()[0]
                
                sql_lnk = """
                    INSERT INTO lnk_seat_on_aircraft (lnk_seat_on_aircraft, hub_seat_key, hub_aircraft_key, lnk_load_dts, lnk_rec_src)
                    VALUES (%s, %s, %s, %s, %s)
                """
                
                cursor.execute(sql_lnk, (l1, l2, result, l4, l5))
                
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

# Flights
def dmp_flights():

    consumer = KafkaConsumer(
        "postgres.public.flights",
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
                h2 = row["flight_id"]
                h3 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                h4 = 'kafka'
                h1 = str(hash(h2) + hash(h3) + hash(h4))
            	
                s1 = h1
                s2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                s3 = ""
                s4 = "kafka"
                s5 = row["flight_no"]
                s6 = row["scheduled_departure"]
                s7 = row["scheduled_arrival"]
                s8 = row["status"]
                s9 = row["actual_departure"]
                s10 = row["actual_arrival"]
                
                l2 = h1
                l3 = row["departure_airport"]
                l4 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                l5 = "kafka"
                l1 = str(hash(l2) + hash(l3) + hash(l4) + hash(l5))
                
                ll2 = h1
                ll3 = row["departure_airport"]
                ll4 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ll5 = "kafka"
                ll6 = str(hash(ll2) + hash(ll3) + hash(ll4) + hash(ll5))
            	
                sql_hub = """
    				INSERT INTO hub_flight (hub_flight_key, hub_flight_bk, hub_load_dts, hub_rec_src)
    				VALUES (%s, %s, %s, %s)
				"""
				
                cursor.execute(sql_hub, (h1, h2, h3, h4))
            	
                sql_sat = """
            		INSERT INTO sat_flight (hub_flight_key, sat_load_dts, hash_diff, sat_rec_src, flight_no, scheduled_departure, scheduled_arrive, status, actual_departure, actual_arrival)
            		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            	"""
                cursor.execute(sql_sat, (s1, s2, s3, s4, s5, s6, s7, s8, s9, s10))
                
                pg_connector.commit()
                
                sub_1 = """
                    SELECT h.hub_airport_key FROM hub_airport as h WHERE h.hub_airport_bk = %s
                """
                
                cursor.execute(sub_1, (l3))
                
                result = str(cursor.fetchone()[0])
                
                sql_lnk = """
                    INSERT INTO lnk_flight_departure_airport (lnk_flight_departure_airport, hub_flight_key, hub_airport_key, lnk_load_dts, lnk_rec_src)
                    VALUES (%s, %s, %s, %s, %s)
                """
                
                cursor.execute(sql_lnk, (l1, l2, result, l4, l5))
                
                pg_connector.commit()
                
                sub_2 = """
                    SELECT h.hub_airport_key FROM hub_airport as h WHERE h.hub_airport_bk = %s
                """
                
                cursor.execute(sub_2, (ll3))
                
                result = str(cursor.fetchone()[0])
                
                sql_lnk = """
                    INSERT INTO lnk_flight_arrive_airport (lnk_flight_arrive_airport, hub_flight_key, hub_airport_key, lnk_load_dts, lnk_rec_src)
                    VALUES (%s, %s, %s, %s, %s)
                """
                
                cursor.execute(sql_lnk, (ll1, ll2, result, ll4, ll5))
                
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
    
# Boardings
def dmp_boardings():

    consumer = KafkaConsumer(
        "postgres.public.boarding_passes",
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
                print("log0")
                h2 = row["boarding_no"]
                h3 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                h4 = 'kafka'
                h1 = str(hash(h2) + hash(h3) + hash(h4))
            	
                s1 = h1
                s2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                s3 = ""
                s4 = "kafka"
                s5 = row["boarding_no"]
                s6 = row["seat_no"]
                
                l2 = h1
                l3 = row["ticket_no"]
                l4 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                l5 = "kafka"
                l1 = str(hash(l2) + hash(l3) + hash(l4) + hash(l5))
                
                print("log1")
                
                sql_hub = """
    				INSERT INTO hub_boarding (hub_boarding_key, hub_boarding_bk, hub_load_dts, hub_rec_src)
    				VALUES (%s, %s, %s, %s)
				"""
				
                cursor.execute(sql_hub, (h1, h2, h3, h4))
                
                print("log2")
            	
                sql_sat = """
            		INSERT INTO sat_flight (hub_boarding_key, sat_load_dts, hash_diff, sat_rec_src, boarding_no, seat_no)
            		VALUES (%s, %s, %s, %s, %s, %s)
            	"""
                cursor.execute(sql_sat, (s1, s2, s3, s4, str(s5), str(s6)))
                
                pg_connector.commit()
                
                sub_1 = """
                    SELECT h.hub_ticket_key FROM hub_ticket as h WHERE h.hub_ticket_bk = %s
                """
                
                print("log3")
                
                cursor.execute(sub_1, (l3))
                
                result = str(cursor.fetchone()[0])
                
                sql_lnk = """
                    INSERT INTO lnk_boarding_matched_with_ticket (lnk_boarding_matched_with_ticket, hub_boarding_key, hub_ticket_key, lnk_load_dts, lnk_rec_src)
                    VALUES (%s, %s, %s, %s, %s)
                """
                
                print("log4")
                
                cursor.execute(sql_lnk, (l1, l2, result, l4, l5))
                
                pg_connector.commit()
                
                print("log5")
                
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
        
# Tickets
def dmp_tickets():

    consumer = KafkaConsumer(
        "postgres.public.tickets",
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
                h2 = row["ticket_no"]
                h3 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                h4 = 'kafka'
                h1 = str(hash(h2) + hash(h3) + hash(h4))
            	
                s1 = h1
                s2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                s3 = ""
                s4 = "kafka"
                s5 = row["ticket_no"]
                s6 = row["passenger_id"]
                s7 = row["passenger_name"]
                s8 = row["contact_data"]
                
                l2 = h1
                l3 = row["book_ref"]
                l4 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                l5 = "kafka"
                l1 = str(hash(l2) + hash(l3) + hash(l4) + hash(l5))
                
                sql_hub = """
    				INSERT INTO hub_ticket (hub_ticket_key, hub_ticket_bk, hub_load_dts, hub_rec_src)
    				VALUES (%s, %s, %s, %s)
				"""
				
                cursor.execute(sql_hub, (h1, h2, h3, h4))
            	
                sql_sat = """
            		INSERT INTO sat_flight (hub_ticket_key, sat_load_dts, hash_diff, sat_rec_src, ticket_no, passenger_id, passenger_name, contact_data)
            		VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            	"""
                cursor.execute(sql_sat, (s1, s2, s3, s4, s5, s6, s7, s8))
                
                pg_connector.commit()
                
                sub_1 = """
                    SELECT h.hub_booking_key FROM hub_booking as h WHERE h.hub_booking_bk = %s
                """
                
                cursor.execute(sub_1, (l3))
                
                result = str(cursor.fetchone()[0])
                
                sql_lnk = """
                    INSERT INTO lnk_ticket_include_booking (lnk_ticket_include_booking_key, hub_ticket_key, hub_booking_key, lnk_load_dts, lnk_rec_src)
                    VALUES (%s, %s, %s, %s, %s)
                """
                
                print("log4")
                
                cursor.execute(sql_lnk, (l1, l2, result, l4, l5))
                
                pg_connector.commit()
                
                print("log5")
                
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

# Booking
def dmp_booking():

    consumer = KafkaConsumer(
        "postgres.public.bookings",
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
                h2 = row["book_ref"]
                h3 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                h4 = 'kafka'
                h1 = str(hash(h2) + hash(h3) + hash(h4))
            	
                s1 = h1
                s2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                s3 = ""
                s4 = "kafka"
                s5 = row["book_date"]
                s6 = row["total_amount"]
                
                sql_hub = """
    				INSERT INTO hub_ticket (hub_ticket_key, hub_ticket_bk, hub_load_dts, hub_rec_src)
    				VALUES (%s, %s, %s, %s)
				"""
				
                cursor.execute(sql_hub, (h1, h2, h3, h4))
            	
                sql_sat = """
            		INSERT INTO sat_flight (hub_ticket_key, sat_load_dts, hash_diff, sat_rec_src, ticket_no, passenger_id, passenger_name, contact_data)
            		VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            	"""
                cursor.execute(sql_sat, (s1, s2, s3, s4, s5, s6, s7, s8))
                
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
    
    dmp_flights_thread = threading.Thread(target=dmp_flights)
    threads.append(dmp_flights_thread)
    dmp_flights_thread.start()
    
    dmp_boardings_thread = threading.Thread(target=dmp_boardings)
    threads.append(dmp_boardings_thread)
    dmp_boardings_thread.start()
    
    dmp_tickets_thread = threading.Thread(target=dmp_tickets)
    threads.append(dmp_tickets_thread)
    dmp_tickets_thread.start()
    
    dmp_booking_thread = threading.Thread(target=dmp_booking)
    threads.append(dmp_booking_thread)
    dmp_booking_thread.start()

main()
