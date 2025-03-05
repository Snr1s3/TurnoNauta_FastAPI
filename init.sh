#!/bin/bash
source venv/bin/activate
uvicorn SRC.main:app --reload