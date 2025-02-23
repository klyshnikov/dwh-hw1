from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime, timedelta

# Определяем аргументы DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Создаем DAG
dag = DAG(
    'copy_data_between_dbs',
    default_args=default_args,
    description='DAG для копирования данных между двумя базами данных',
    schedule_interval=timedelta(days=1),
)

# Функция для копирования данных
def copy_data():
    # Инициализируем подключение к источнику
    source_hook = PostgresHook(postgres_conn_id='source_db')
    source_conn = source_hook.get_conn()
    source_cursor = source_conn.cursor()

    # Инициализируем подключение к целевой базе данных
    target_hook = PostgresHook(postgres_conn_id='target_db')
    target_conn = target_hook.get_conn()
    target_cursor = target_conn.cursor()
    
    # Создаем таблицы в схеме public
    #source_cursor.execute("CREATE TABLE IF NOT EXISTS source_table (id integer)")
    target_cursor.execute("CREATE TABLE IF NOT EXISTS flights (flight_id serial PRIMARY KEY, flight_no char(6), scheduled_departure timestamptz, scheduled_arrival timestamptz, departure_airport char(3) references airports(airport_code), arrival_airport char(3) references airports(airport_code), status varchar(20), aircraft_code varchar(3) references aircafts(aircraft_code), actual_departure timestamptz, actual_arrival timestamptz)")
    #source_cursor.execute("INSERT INTO source_table (id) VALUES (1)")

    # Пример SQL-запроса для выборки данных из источника
    source_cursor.execute("SELECT * FROM flights(flight_id, flight_no, scheduled_departure, scheduled_arrival, departure_airport, arrival_airport, status, aircraft_code, actual_departure, actual_arrival)")
    rows = source_cursor.fetchall()

    # Вставляем данные в целевую таблицу
    for row in rows:
        target_cursor.execute("INSERT INTO flights VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)

    # Коммитим изменения
    source_conn.commit()
    target_conn.commit()

    # Закрываем подключения
    source_cursor.close()
    source_conn.close()
    target_cursor.close()
    target_conn.close()

# Создаем задачу в DAG
copy_data_task = PythonOperator(
    task_id='copy_data',
    python_callable=copy_data,
    dag=dag,
)

# Определяем порядок выполнения задач
copy_data_task
