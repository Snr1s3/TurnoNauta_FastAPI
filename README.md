# TurnoNauta_FastAPI


## Python enviroment
source venv/bin/activate

## Run API
uvicorn main:app --reload

## Check ip container 
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgresProj



openssl req -x509 -newkey rsa:4096 -keyout ./TurnoNauta_FastAPI/SRC/ssl/key.pem -out ./TurnoNauta_FastAPI/SRC/ssl/cert.pem -days 3650 -nodes

--port 443 --ssl-keyfile ./TurnoNauta_FastAPI/ssl/key.pem --ssl-certfile ./TurnoNauta_FastAPI/SRC/ssl/cert.pem


## Links

- [MOBIL]([https://github.com/Snr1s3/TurnoNauta_FastAPI.git](https://github.com/Snr1s3/Turnonauta.git))
- [WEB](https://github.com/EdwindanielTIC/web_TurnoNauta.git)
