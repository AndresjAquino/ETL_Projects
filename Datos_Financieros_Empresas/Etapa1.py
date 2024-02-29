from fmp_python.fmp import FMP
import json
from sqlalchemy import create_engine
from decouple import config

# API key
fmp = FMP(api_key='a6f7a1b79e3bdcf8cff1abd40b8105cd')

# símbolos de empresas
symbols = ['AAL','AAPL','GOOGL','AMZN','MSFT','TSLA','META','NVDA','JPM','GS']

# diccionario para almacenar datos de las empresas
empresa_data = {}

# iteraración de la lista de símbolos para obtener los datos de cada empresa
for symbol in symbols:
    data = fmp.get_quote(symbol)
    print(f'Datos de {symbol}: {data}')
    
    # se agregan los datos al diccionario
    empresa_data[symbol] = data

# se guarda en un archivo json
with open('empresa_data.json','w') as json_file:
    json.dump(empresa_data, json_file)

# Credenciales desde el archivo .env
username = config('DB_USERNAME')
password = config('DB_PASSWORD')
host = config('DB_HOST')
port = config('DB_PORT')
database_name = config('DB_NAME')

# URL de conexión
url = f'postgresql://{username}:{password}@{host}:{port}/{database_name}'

# Conexión a la base de datos
conn = create_engine(url)
