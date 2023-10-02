from fmp_python.fmp import FMP
import json
from sqlalchemy import create_engine, text
from decouple import config
import pandas as pd

# Configuración
API_KEY = 'a6f7a1b79e3bdcf8cff1abd40b8105cd'
SYMBOLS = ['AAL', 'AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA', 'META', 'NVDA', 'JPM', 'GS']

# Función para obtener datos de una empresa y almacenarlos en el diccionario
def obtener_datos_empresa(api, symbol):
    data = api.get_quote(symbol)
    print(f'{symbol}: {data}')
    return data[0]

# Diccionario para almacenar datos de las empresas
empresa_data = {}

# Obtener y almacenar datos de cada empresa
fmp = FMP(api_key=API_KEY)
for symbol in SYMBOLS:
    empresa_data[symbol] = obtener_datos_empresa(fmp, symbol)

# Guardar datos en un archivo JSON
with open('empresa_data.json', 'w') as json_file:
    json.dump(empresa_data, json_file)

# Leer json y cargar en un DataFrame
with open('empresa_data.json', 'r') as json_file:
    empresa_data = json.load(json_file)

# Convertir el diccionario en un DataFrame
df = pd.DataFrame.from_dict(empresa_data).T  # Transponer el DataFrame
df.index.name = 'symbol'  # Cambiar el nombre del índice

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
conn = create_engine(url, pool_pre_ping=True)

# Exportar el DataFrame a la base de datos
df.to_sql('empresa_data', conn, if_exists='replace', index=False)

# Cierro la conexión a la base de datos
conn.close()