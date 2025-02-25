from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'presentation_copy_data',
    default_args=default_args,
    description='Собирает витрину из postgres_master в postgres_2 схеме presentation',
    schedule_interval=timedelta(days=1),
)

def add_presentation_data():
    source_hook = PostgresHook(postgres_conn_id='source_db')
    source_conn = source_hook.get_conn()
    source_cursor = source_conn.cursor()

    target_hook = PostgresHook(postgres_conn_id='target_db')
    target_conn = target_hook.get_conn()
    target_cursor = target_conn.cursor()
    
    target_cursor.execute("\
    CREATE TABLE IF NOT EXISTS presentation ( \
    	created_at timestamptz,\
    	passenger_id varchar(20),\
    	passenger_name text,\
    	flight_number int,\
    	purchase_sum int,\
    	home_airport text ) ")

    query_presentation = "\
    SELECT DISTINCT ON (t.passenger_id) \
    	NOW() as created_at, \
    	t.passenger_id as passenger_id, \
    	t.passenger_name as passenger_name, \
    	COUNT(DISTINCT f.flight_id) AS flight_number, \
    	SUM(b.total_amount) AS purchase_sum, \
    	a.airport_name as home_airport \
	FROM tickets t \
	JOIN bookings b ON t.book_ref = b.book_ref \
	JOIN ticket_flights tf ON tf.ticket_no = t.ticket_no \
	JOIN flights f ON f.flight_id = tf.flight_id \
	JOIN airports a ON a.airport_code = f.departure_airport OR a.airport_code = f.arrival_airport \
	GROUP BY \
    	t.passenger_id, \
    	t.passenger_name, \
    	a.airport_name \
	ORDER BY \
    	t.passenger_id, \
    COUNT(DISTINCT f.flight_id) DESC;"
    
    source_cursor.execute(query_presentation)
    rows = source_cursor.fetchall()

    for row in rows:
        target_cursor.execute("INSERT INTO presentation VALUES (%s, %s, %s, %s, %s, %s)", row)

    source_conn.commit()
    target_conn.commit()

    source_cursor.close()
    source_conn.close()
    target_cursor.close()
    target_conn.close()

presentation_task = PythonOperator(
    task_id='add_presentation_data',
    python_callable=add_presentation_data,
    dag=dag,
)

# Тут будет всего одна операция - сбор данных из мастера и созданние данных для витрины
# Т.к я не понял, как даги могут общаться между собой или перекидывать данные
presentation_task
