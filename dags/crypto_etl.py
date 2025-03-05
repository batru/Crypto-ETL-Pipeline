from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import requests
import json
from datetime import datetime, timedelta

default_args = {
    'owner':'Airflow',
    'depends_on_past':False,
    'start_date': datetime(2025, 3, 3),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'Crypto_etl',
    default_args= default_args,
    description= 'Crpto ETL',
    schedule_interval = timedelta(hours=1),
    catchup = False,
)

def fetch_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    with open("/tmp/crypto_prices.json", "w") as f:
        json.dump(data, f)

def transform_data():
    with open("/tmp/crypto_prices.json", "r") as f:
        data = json.load(f)

    transform_data = [
        ("bitcoin", data["bitcoin"]["usd"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ("ethereum", data["ethereum"]["usd"], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    ]

    with open("/tmp/crypto_prices.json", "w") as f:
        json.dump(transform_data, f)

def load_to_postgres():
    hook = PostgresHook(postgres_conn_id='aiven_postgres')
    conn = hook.get_conn()
    cursor = conn.cursor()

    with open("/tmp/crypto_prices.json", "r") as f:
        transform_data = json.load(f)
    
    for crypto, price, timestamp in transform_data:
        cursor.execute( """ 
            INSERT INTO crypto_prices (crypto, price, timestamp)
            values (%s, %s, %s);
        """, (crypto, price, timestamp)
        )

    conn.commit()
    cursor.close()
    conn.close()

task_fetch = PythonOperator(
        task_id = 'fetch_crypto_prices',
        python_callable= fetch_crypto_prices,
        dag=dag,
    )

task_transform = PythonOperator(
        task_id= 'transform_data',
        python_callable= transform_data,
        dag=dag,
    )

task_load = PythonOperator(
        task_id= 'load_to_postgres',
        python_callable= load_to_postgres,
        dag=dag,
    )

task_fetch >> task_transform >> task_load


       





