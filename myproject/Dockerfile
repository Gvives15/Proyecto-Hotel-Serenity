# Usar la imagen oficial de Python
FROM python:3.11

# Crear un directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar solo requirements.txt primero
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto al contenedor
COPY . .

# Exponer el puerto 8000 para Django
EXPOSE 8000

# Comando para correr el servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
