# Usa una imagen base oficial de Python
FROM python:3.12-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt en el directorio de trabajo
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido de tu aplicación en el directorio de trabajo
COPY . .

# Expone el puerto en el que la aplicación correrá
EXPOSE 5000

# Establece la variable de entorno para Flask
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Comando para ejecutar la aplicación
CMD ["flask", "run"]
