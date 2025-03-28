#!/bin/bash
sudo apt-get update

sudo apt-get install -y python3 python3-venv python3-pip 

python3 -m venv ./venv

source ./venv/bin/activate

pip install -r ./TurnoNauta_FastAPI/requirements.txt

pip install --upgrade pip

bash ./init.sh