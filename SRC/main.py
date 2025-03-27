from fastapi import FastAPI, HTTPException, Depends
from typing import List
from fastapi.staticfiles import StaticFiles
from .client import get_db_connection, release_db_connection
from .models import Emparellaments, Estadistiques, Format, Puntuacio, Rang, Resultat, Rol, Ronda, Subscripcio, Torneig, Usuaris, UserStatistics, NewUser
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


#####################################       Login        #####################################

@app.get("/login")
def login(username: str, password: str):
    return verify_user_credentials(username, password)

##################################### Pantall Benvinguda #####################################

@app.get("/user_statistics")
def get_user_statistics(user_id: int):
    return verify_user_statistics(user_id)

#####################################   Tornejos Jugats  #####################################

@app.get("/tournaments_played", response_model=List[Torneig])
def get_tournaments_played_endpoint(user_id: int):
    return get_tournaments_played(user_id)

#####################################     User per ID    #####################################

@app.get("/user_by_id", response_model=Usuaris)
def get_user_by_id(user_id: int):
    return get_usuari_id(user_id)

#####################################   Torneig per ID   #####################################

@app.get("/tournament_by_id", response_model=Torneig)
def get_tournament_by_id(torneig_id: int):
    return get_tournament_id(torneig_id)

#####################################  Puntuacio Torneig #####################################

@app.get("/users_in_tournament", response_model=List[UserWithPoints])
def get_users_in_tournament(torneig_id: int):
    return get_users_points(torneig_id)

#####################################   Afegir Usuari    #####################################

@app.post("/add_user", response_model=Usuaris)
def add_user(user: NewUser):
    return add_usuari(user)



@app.get("/usuaris/", response_model=List[Usuaris])
def get_usuaris_all():
    return get_usuaris()






"""
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


"""