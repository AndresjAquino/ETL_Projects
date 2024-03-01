# I M P O R T A C I Ó N    D E    L I B R E R I A S
import requests
import pandas as pd
from sqlalchemy import create_engine
from decouple import config
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# D E F I N I C I Ó N    D E L    D A G
default_args = {
    'owner': 'AndresAquino',
    'start_date': datetime(2023, 10, 2),
    'retries': 1,
}

dag = DAG(
    'cargar_datos_empresas',
    default_args=default_args,
    schedule_interval=None,  # Programar la ejecución según tus necesidades
    dag_id='Dag_Entrega3',
    description= '',
    start_date=datetime(2023,10,1,2),
    schedule_interval='@daily'
)

# Lista de tickers que deseas consultar
tickers = ['AAL', 'AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA', 'META', 'NVDA', 'JPM', 'GS']
api_key = 'a6f7a1b79e3bdcf8cff1abd40b8105cd'
# Configurar la URL base
base_url = 'https://financialmodelingprep.com/api'
base_type = 'income-statement'


# F U N C I O N E S
# Función para obtener datos de una empresa
def obtener_datos_empresa(ticker):
    url = f'{base_url}/v3/{base_type}/{ticker}?apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data, ticker

# Función para guardar datos en un archivo json
def guardar_datos_json(data):
    result_df = pd.DataFrame()
    for data_item, ticker in data:
        if data_item:
            df = pd.DataFrame(data_item)
            df['Ticker'] = ticker
            result_df = pd.concat([result_df, df], ignore_index=True)

    result_df.to_json('datos_empresas.json', orient='records', lines=True)

# Función para exportar datos a la base de datos
def exportar_a_base_de_datos():
    username = config('DB_USERNAME')
    password = config('DB_PASSWORD')
    host = config('DB_HOST')
    port = config('DB_PORT')
    database_name = config('DB_NAME')

    engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database_name}')
    result_df = pd.read_json('datos_empresas.json', orient='records', lines=True)
    result_df.to_sql('datos_empresas', engine, schema='andresjaquino_coderhouse', if_exists='replace', index=False)
    engine.dispose()

# T A R E A S    D E L    D A G
obtener_datos = PythonOperator(
    task_id='obtener_datos_empresas',
    python_callable=obtener_datos_empresa,
    op_args=[tickers],
    dag=dag,
)

guardar_json = PythonOperator(
    task_id='guardar_datos_json',
    python_callable=guardar_datos_json,
    provide_context=True,
    dag=dag,
)

exportar_bd = PythonOperator(
    task_id='exportar_a_base_de_datos',
    python_callable=exportar_a_base_de_datos,
    dag=dag,
)

# O R D E N    D E    E J E C U C I Ó N    D E   L A S   T A R E A S
obtener_datos >> guardar_json >> exportar_bd
