import requests
import psycopg2
from decouple import config

# Lista de tickers que deseas consultar
tickers = ['AAL', 'AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA', 'META', 'NVDA', 'JPM', 'GS']
api_key = 'a6f7a1b79e3bdcf8cff1abd40b8105cd'

# Configurar la URL base
base_url = 'https://financialmodelingprep.com/api'
base_type = 'income-statement'

# Inicializar una lista para almacenar los datos
data_list = []

# Recorrer los tickers y obtener los datos para cada uno
for ticker in tickers:
    url = f'{base_url}/v3/{base_type}/{ticker}?apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    if data:
        # Modificar cada diccionario en la lista para agregar la clave 'Ticker'
        for item in data:
            item['Ticker'] = ticker
        data_list.extend(data)  # Extender la lista con los datos modificados

# Credenciales desde el archivo .env
username = config('DB_USERNAME')
password = config('DB_PASSWORD')
host = config('DB_HOST')
port = config('DB_PORT')
database_name = config('DB_NAME')

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    database=database_name,
    user=username,
    password=password,
    host=host,
    port=port
)
cursor = conn.cursor()

# Insertar los datos en la tabla "datos_empresas"
for data in data_list:
    try:
       cursor.execute(
    """
    INSERT INTO andresjaquino_coderhouse.datos_empresas (
        date,
        symbol,
        reportedCurrency,
        cik,
        fillingDate,
        acceptedDate,
        calendarYear,
        period,
        revenue,
        costOfRevenue,
        grossProfit,
        grossProfitRatio,
        researchAndDevelopmentExpenses,
        generalAndAdministrativeExpenses,
        sellingAndMarketingExpenses,
        sellingGeneralAndAdministrativeExpenses,
        otherExpenses,
        operatingExpenses,
        costAndExpenses,
        interestIncome,
        interestExpense,
        depreciationAndAmortization,
        ebitda,
        ebitdaratio,
        operatingIncome,
        operatingIncomeRatio,
        totalOtherIncomeExpensesNet,
        incomeBeforeTax,
        incomeBeforeTaxRatio,
        incomeTaxExpense,
        netIncome,
        netIncomeRatio,
        eps,
        epsdiluted,
        weightedAverageShsOut,
        weightedAverageShsOutDil,
        link,
        finalLink,
        Ticker
    )
    VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s
    )
    """,
    (
        data['date'],
        data['symbol'],
        data['reportedCurrency'],
        data['cik'],
        data['fillingDate'],
        data['acceptedDate'],
        data['calendarYear'],
        data['period'],
        data['revenue'],
        data['costOfRevenue'],
        data['grossProfit'],
        data['grossProfitRatio'],
        data['researchAndDevelopmentExpenses'],
        data['generalAndAdministrativeExpenses'],
        data['sellingAndMarketingExpenses'],
        data['sellingGeneralAndAdministrativeExpenses'],
        data['otherExpenses'],
        data['operatingExpenses'],
        data['costAndExpenses'],
        data['interestIncome'],
        data['interestExpense'],
        data['depreciationAndAmortization'],
        data['ebitda'],
        data['ebitdaratio'],
        data['operatingIncome'],
        data['operatingIncomeRatio'],
        data['totalOtherIncomeExpensesNet'],
        data['incomeBeforeTax'],
        data['incomeBeforeTaxRatio'],
        data['incomeTaxExpense'],
        data['netIncome'],
        data['netIncomeRatio'],
        data['eps'],
        data['epsdiluted'],
        data['weightedAverageShsOut'],
        data['weightedAverageShsOutDil'],
        data['link'],
        data['finalLink'],
        data['Ticker']
    )
)

    except Exception as e:
        print(f"Error al insertar datos: {str(e)}")

# Confirmar y cerrar la conexión a la base de datos
conn.commit()
conn.close()

