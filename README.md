# power_back_end

## Instalacion
En tu consola de comandos ejecuta el siguiente comando para instalar las dependencias
```bash
pip install -r requirements.txt
```

## Configuracion
1. Crea un archivo llamado `.env` en la raiz del proyecto
2. Agrega las siguientes variables de entorno en el archivo `.env`
```bash
# Configuracion de la base de datos 
DB_HOST=localhost
DB_PORT=543
DB_NAME=power
DB_USER=postgres
DB_PASSWORD=postgres
```
puedesver de referencia el archivo `.env.example` para ver como debe quedar el archivo `.env`

## Levantar el servidor
```bash
uvicorn app:app --reload --port 8000
```
y podras acceder a la documentacion de la API en `http://localhost:8000/docs`