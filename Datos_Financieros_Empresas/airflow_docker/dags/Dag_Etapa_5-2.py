import requests
import pandas as pd
from sqlalchemy import create_engine
from decouple import config
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.models import Variable
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

# Definir el DAG
default_args = {
    'owner': 'AndresAquino',
    'start_date': datetime(2023, 10, 2),
    'email': ['andresjaquino@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
}

dag = DAG(
    'cargar_datos_empresas',
    default_args=default_args,
    description= '',
    schedule_interval='@daily',
)

# Lista de tickers que deseas consultar
tickers = ['AAL', 'AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA', 'META', 'NVDA', 'JPM', 'GS']
api_key = 'a6f7a1b79e3bdcf8cff1abd40b8105cd'

# Configurar la URL base
base_url = 'https://financialmodelingprep.com/api'
base_type = 'income-statement'

# Función para obtener datos de empresas
def obtener_datos_empresa(ticker):
    url = f'{base_url}/v3/{base_type}/{ticker}?apikey={api_key}'
    response = requests.get(url)
    data = response.json()

    if not data:
        print(f"No se encontraron datos para el ticker {ticker}")
    else:
        print(f"Datos obtenidos para el ticker {ticker}")

    return data, ticker

# Función para guardar datos en un archivo json
def guardar_datos_json(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='obtener_datos_empresas')  # Recupera los datos de la tarea obtener_datos_empresas
    if not data:
        raise ValueError("No se encontraron datos para guardar.")
    
    result_df = pd.DataFrame()
    for data_item in data:
        if data_item:
            df = pd.DataFrame(data_item)
            result_df = pd.concat([result_df, df], ignore_index=True)
    
    if result_df.empty:
        raise ValueError("No se encontraron datos válidos para guardar.")
    
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

# Tareas del DAG
obtener_datos = PythonOperator(
    task_id='obtener_datos_empresas',
    python_callable=obtener_datos_empresa,
    op_args=[tickers],
    provide_context=True,  # Necesario para que pueda almacenar datos en XCom
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

# alerta por correo electrónico
email_task = EmailOperator(
    dag=dag,
    task_id='send_email',
    to='andresjaquino@gmail.com',
    subject= 'Datos de empresas',
    html_content="Proceso de carga de datos se ha completado con éxito."
)

# Orden de ejecución de las tareas
obtener_datos >> guardar_json >> exportar_bd >> email_task
