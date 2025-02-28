from fastapi import FastAPI, HTTPException, Depends
from client import get_db_connection
from models import *
from datetime import date
from typing import List


###################################
## GETS DE TOTA LA BASE DE DADES ##
###################################
from emparellaments.gets_emparellaments import *
from estadistiques.gets_estadistiques import *
from formats.gets_formats import *
from jugadors.gets_jugadors import *
from puntuacions.gets_puntuacions import *
from rangs.gets_rangs import *
from resultats.gets_resultats import *
from rols.gets_rols import *
from rondes.gets_rondes import *
from rondes_torneig.gets_rondes_torneig import *
from subscripcions.gets_subscripcions import *
from tornejos.gets_tornejos import *
from usuaris.gets_usuaris import *


app = FastAPI()

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

@app.get("/jugadors/", response_model=List[Jugadors])
def get_jugadors_all():
    return get_jugadors()
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

@app.get("/rondes_torneig/", response_model=List[Rondes_Torneig])
def get_rondes_torneig_all():
    return get_rondes_torneig()

@app.get("/subscripcions/", response_model=List[Subscripcio])
def get_subscripcions_all():
    return get_subscripcions()

@app.get("/tornejos/", response_model=List[Torneig])
def get_tornejos_all():
    return get_torneig()

@app.get("/usuaris/", response_model=List[Usuaris])
def get_usuaris_all():
    return get_usuaris()

