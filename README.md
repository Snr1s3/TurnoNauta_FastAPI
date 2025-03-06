# TurnoNauta_FastAPI


## Python enviroment
source venv/bin/activate

## Run API
uvicorn main:app --reload

## Check ip container 
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgresProj