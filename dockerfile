# imagen base de Python
FROM python:3.8

# Instalo dependencias necesarias
RUN pip install requests
RUN pip install pandas 
RUN pip install sqlalchemy==1.4.49 
RUN pip install python-decouple
RUN pip install psycopg2-binary

# Directorio de trabajo en /app
WORKDIR /app

# Copio script y el archivo .env a la imagen
COPY Entrega2.py .env ./

# Ejecuto el código Python cuando se inicie el contenedor
CMD ["python", "Entrega2.py"]