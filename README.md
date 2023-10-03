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
   
   Archivo con nombre "dockerfile"

   Pasos para correrlo

       Bash
   
       docker build -t entrega3 . # Construcción imagen
   
       docker run entrega3 # Corre el contenedor a partir de la imagen

3) Se entrega un DAG de Apache Airflow utilizando PythonOperator

   Archivo Dag con nombre "Dag_Entrega3", en carpeta airflow_docker/dags

   Pasos para correrlo
   
       Bash
   
       docker-compose up
   
   orden de ejecución de las tareas
       
       obtener_datos >> guardar_json >> exportar_bd
