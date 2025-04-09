from fastapi import FastAPI, HTTPException, Depends
from typing import List
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


#####################################      Usuaris       #####################################

@app.get("/users/", response_model=List[Usuaris])
def get_usuaris_all():
    return get_usuaris()

#####################################  Puntuacio Torneig #####################################

@app.get("/users/users_in_tournament", response_model=List[UserWithPoints])
def get_users_in_tournament(torneig_id: int):
    return get_users_points(torneig_id)

##################################### Usuaris check nom  #####################################

@app.get("/users/check_username", response_model=bool)
def check_username_exists(username: str):
    return check_username(username)

#####################################       Login        #####################################

@app.get("/users/login")
def login(username: str, password: str):
    return verify_user_credentials(username, password)

##################################### Pantall Benvinguda #####################################

@app.get("/users/user_statistics")
def get_user_statistics(user_id: int):
    return verify_user_statistics(user_id)

#####################################     User per ID    #####################################

@app.get("/users/get_by_id", response_model=Usuaris)
def get_user_by_id(user_id: int):
    return get_usuari_id(user_id)

#####################################   Tornejos Jugats  #####################################

@app.get("/tournaments/tournaments_played", response_model=List[Torneig])
def get_tournaments_played_endpoint(user_id: int):
    return get_tournaments_played(user_id)

#####################################   Torneig per ID   #####################################

@app.get("/tournaments/tournament_by_id", response_model=Torneig)
def get_tournament_by_id(torneig_id: int):
    return get_tournament_id(torneig_id)

#####################################   Tornejos Actius   #####################################

@app.get("/tournaments/active", response_model=List[Torneig])
def get_active_tournaments():
    return get_active_tournaments_from_db()

#####################################   Afegir Usuari    #####################################

@app.post("/users/add_user", response_model=Usuaris)
def add_user(user: NewUser):
    return add_usuari(user)
    
##################################### Usuaris update nom #####################################

@app.put("/users/update_name/{user_id}", response_model=Usuaris)
def update_user_name(user_id: int, new_name: str):
    return update_username(user_id, new_name)

#################################### Delete Usuaris  #########################################
@app.delete("/users/delete_by_id", response_model=bool)
def delete_user_by_id(user_id: int):
    return delete_user_id(user_id)
    
"""
##################################### GET METHODS #####################################



#####################################      FAST AP        #####################################

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