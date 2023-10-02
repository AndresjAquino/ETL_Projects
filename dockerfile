# imagen base de Python
FROM python:3.8

# Instalo dependencias necesarias
RUN pip install fmp-python 
RUN pip install sqlalchemy 
RUN pip install decouple 
RUN pip install pandas 
RUN pip install psycopg2-binary

# Directorio de trabajo en /app
WORKDIR /app

# Copio script y el archivo .env a la imagen
COPY Entrega2.py .env ./

# Ejecuto el código Python cuando se inicie el contenedor
CMD ["python", "Entrega2.py"]