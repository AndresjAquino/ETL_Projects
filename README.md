# Entrega 1

1) Se desarrolla un script que extrae datos de una API pública.
    
      API: https://site.financialmodelingprep.com/

2) Se extraen los datos financieros de 10 empresas
   
    • American Airlines Group Inc. "AAL"

    • Apple Inc "AAPL"

    • Alphabet Inc "GOOGL"

    • Amazon.com, Inc. "AMZN"

    • Microsoft Corporation "MSFT"

    • Tesla, Inc ""TSLA"

    • Meta Platforms, Inc. "META"

    • NVIDIA Corporation "NVDA"

    • JPMorgan Chase & Co. "JPM"

    • The Goldman Sachs Group, Inc. "GS"


3) Se crea una conexión a Redshift para posterior carga de los datos extraidos.

# Entrega 2

1) Se crea tabla en Redshift

3) Cargar los datos leídos de la API en la tabla.

# Entrega 3

1) Se entrega un dockerfile para crear una imagen y un contenedor

3) Se entrega un DAG de Apache Airflow utilizando PythonOperator

       Ejecuta 3 tareas: obtener_datos >> guardar_json >> exportar_bd
