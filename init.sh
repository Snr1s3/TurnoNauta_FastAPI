#!/bin/bash
source ./TurnoNauta_FastAPI/venv/bin/activate
uvicorn SRC.main:app --reload