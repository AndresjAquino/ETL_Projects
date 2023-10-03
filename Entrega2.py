import requests
import pandas as pd
from sqlalchemy import create_engine
from decouple import config

# Lista de tickers que deseas consultar
tickers = ['AAL', 'AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA', 'META', 'NVDA', 'JPM', 'GS']
api_key = 'a6f7a1b79e3bdcf8cff1abd40b8105cd'

# Inicializar un DataFrame vacío para almacenar los datos
result_df = pd.DataFrame()

# Configurar la URL base
base_url = 'https://financialmodelingprep.com/api'
base_type = 'income-statement'

# Recorrer los tickers y obtener los datos para cada uno
for ticker in tickers:
    url = f'{base_url}/v3/{base_type}/{ticker}?apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    if data:
        # Crear un DataFrame con los datos y agregar una columna "Ticker" para identificar la empresa
        df = pd.DataFrame(data)
        df['Ticker'] = ticker
        
        # Concatenar el DataFrame actual con el resultado acumulado
        result_df = pd.concat([result_df, df], ignore_index=True)

# Mostrar el DataFrame resultante con los datos de todas las empresas
result_df

# Guardar el DataFrame en un archivo JSON
result_df.to_json('datos_empresas.json', orient='records', lines=True)

# Credenciales desde el archivo .env
username = config('DB_USERNAME')
password = config('DB_PASSWORD')
host = config('DB_HOST')
port = config('DB_PORT')
database_name = config('DB_NAME')

# conexión
engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database_name}')

# Exportar el DataFrame a la base de datos
result_df.to_sql('datos_empresas', engine, schema='andresjaquino_coderhouse', if_exists='replace', index=False)

# Cierro la conexión a la base de datos
engine.dispose()