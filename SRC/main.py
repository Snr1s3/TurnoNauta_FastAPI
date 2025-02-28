from fastapi import FastAPI, HTTPException, Depends
from client import get_db_connection
from models import IncomeCreate, Income, ExpenseCreate, Expense
from datetime import date
import mysql.connector

app = FastAPI()


@app.get("/docs")
