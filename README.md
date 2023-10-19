# Entrega 1

**1. Desarrollo de un script para extraer datos de una API pública.**

   API: [https://site.financialmodelingprep.com/]

**2. Extracción de datos financieros de 10 empresas:**

   - American Airlines Group Inc. "AAL"
   - Apple Inc "AAPL"
   - Alphabet Inc "GOOGL"
   - Amazon.com, Inc. "AMZN"
   - Microsoft Corporation "MSFT"
   - Tesla, Inc "TSLA"
   - Meta Platforms, Inc. "META"
   - NVIDIA Corporation "NVDA"
   - JPMorgan Chase & Co. "JPM"
   - The Goldman Sachs Group, Inc. "GS"

**3. Creación de una conexión a Redshift para la carga posterior de los datos extraídos.**

# Entrega 2

**1. Creación de una tabla en Redshift.**

**2. Carga de los datos leídos de la API en la tabla.**

# Entrega 3

**1. Entrega de un Dockerfile para crear una imagen y un contenedor.**

   - Archivo con nombre "dockerfile".

   - Pasos para ejecutarlo:

     ```bash
     docker build -t entrega3 . # Construcción de la imagen
     docker run entrega3 # Ejecución del contenedor a partir de la imagen
     ```

**2. Entrega de un DAG de Apache Airflow utilizando PythonOperator.**

   - Archivo DAG con nombre "Dag_Entrega3", ubicado en la carpeta `airflow_docker/dags`.

   - Parámetros:

     ```python
     # Definir el DAG
     default_args = {
         'owner': 'AndresAquino',
         'start_date': datetime(2023, 10, 2),
         'retries': 1,
     }

     dag = DAG(
         'cargar_datos_empresas',
         default_args=default_args,
         schedule_interval=None, 
         dag_id='Dag_Entrega3',
         description='',
         start_date=datetime(2023, 10, 1, 2),
         schedule_interval='@daily'
     )
     ```

   - Pasos para ejecutarlo:

     ```bash
     docker-compose up
     ```

   - Orden de ejecución de las tareas: `obtener_datos >> guardar_json >> exportar_bd`

# Entrega 4

**1. Se incorpora al proyecto el envío de alertas mediante SMTP.**

   - En el archivo Dag_Entrega4.py, ubicado en la carpeta de dags:

   - Se importa el operador EmailOperator

         from airflow.operators.email import EmailOperator
 
   - Se incorpora la Tarea email_task

         # alerta por correo electrónico
         email_task = EmailOperator(
              task_id='send_email',
              to="andresjaquino@gmail.com",
              subject= "Datos de empresas",
              html_content="""<h3>Proceso de carga de datos se ha completado con éxito.</h3>""",
              dag=dag,
              )

**2. Se adjunta captura de pantalla de las alertas y del proceso en Airflow.**

   - Gmail
     
   - DGAs

   - Grid

   - Graph
