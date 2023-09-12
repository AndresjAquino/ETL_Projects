from fmp_python.fmp import FMP
import json
from sqlalchemy import create_engine
from decouple import config
import psycopg2
import pandas as pd

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
    empresa_data[symbol] = data[0] #data[0] para traer el primer elemento de la lista

# se guarda en un archivo json
with open('empresa_data.json','w') as json_file:
    json.dump(empresa_data, json_file)

# Leer json y cargar en un DataFrame
with open('empresa_data.json', 'r') as json_file:
    empresa_data = json.load(json_file)

# Convertir el diccionario en un DataFrame
df = pd.DataFrame.from_dict(empresa_data).T  # Transponer el DataFrame

# symbol como índice del DataFrame
df.set_index('symbol', inplace=True)

# Columnas deseadas
columnas = [
    'symbol', 'name', 'price', 'changesPercentage', 'change',
    'dayLow', 'dayHigh', 'yearHigh', 'yearLow', 'marketCap',
    'priceAvg50', 'priceAvg200', 'exchange', 'volume', 'avgVolume',
    'open', 'previousClose', 'eps', 'pe', 'earningsAnnouncement',
    'sharesOutstanding', 'timestamp']

df = df[columnas]

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

# Exporto el DataFrame a la base de datos
df.to_sql('empresa_data', conn, if_exists='replace', index=False)

# Cierro la conexión a la base de datos
conn.close()