#!/bin/bash
source ./venv/bin/activate

./venv/bin/uvicorn SRC.main:app --reload --host 0.0.0.0 --port 6000