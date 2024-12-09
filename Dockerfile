# Usa una imagen base de Python
FROM python:3.12

# Establece el directorio de trabajo en el contenedor
WORKDIR /usr/src/app

# Copia el archivo de requisitos y instala las dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido del proyecto al directorio de trabajo
COPY . .

# Establece la variable de entorno para Flask
ENV FLASK_APP=run.py

# Expone el puerto en el que correrá la aplicación Flask
EXPOSE 5000

# Define el comando para correr la aplicación
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]