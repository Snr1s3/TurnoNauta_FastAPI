from fastapi import FastAPI, HTTPException, Depends
from typing import List
from fastapi.staticfiles import StaticFiles
from .client import get_db_connection, release_db_connection
from .models import Emparellaments, Estadistiques, Format, Puntuacio, Rang, Resultat, Rol, Ronda, Subscripcio, Torneig, Usuaris
from datetime import date
from .schemas import LoginRequest

from .routers.emparellaments import *
from .routers.estadistiques import *
from .routers.formats import *
from .routers.puntuacions import *
from .routers.rangs import *
from .routers.resultats import *
from .routers.rols import *
from .routers.rondes import *
from .routers.subscripcions import *
from .routers.tornejos import *
from .routers.usuaris import *

app = FastAPI()


##################################### GET METHODS #####################################
@app.get("/")
def read_docs():
    return {"message": "Turnonauta API"}

@app.get("/docs")
def read_docs():
    return {"message": "This is the documentation endpoint."}


@app.get("/emparellaments/", response_model=List[Emparellaments])
def get_emparellaments_all():
    return get_emparellaments()

@app.get("/estadistiques/", response_model=List[Estadistiques])
def get_estadistiques_all():
    return get_estadistiques()

@app.get("/formats/", response_model=List[Format])
def get_formats_all():
    return get_formats()

@app.get("/puntauacions/", response_model=List[Puntuacio])
def get_puntuacions_all():
    return get_puntuacions()

@app.get("/rangs/", response_model=List[Rang])
def get_rangs_all():
    return get_rangs()

@app.get("/resultats/", response_model=List[Resultat])
def get_resultats_all():
    return get_resultats()

@app.get("/rols/", response_model=List[Rol])
def get_rols_all():
    return get_rols()

@app.get("/rondes/", response_model=List[Ronda])
def get_rondes_all():
    return get_rondes()

@app.get("/subscripcions/", response_model=List[Subscripcio])
def get_subscripcions_all():
    return get_subscripcions()

@app.get("/tornejos/", response_model=List[Torneig])
def get_tornejos_all():
    return get_torneig()

@app.get("/usuaris/", response_model=List[Usuaris])
def get_usuaris_all():
    return get_usuaris()

##################################### POST METHODS #####################################
@app.get("/login")
def login(username: str, password: str):
    return verify_user_credentials(username, password)