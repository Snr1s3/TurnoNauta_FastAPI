from fastapi import FastAPI, HTTPException, Depends
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .client import get_db_connection, release_db_connection
from .models import *
from datetime import date

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

########################################      Puntuacio    #####################################
@app.get("/puntauacions/", response_model=List[Puntuacio])
def get_puntuacions_all():
    return get_puntuacions()

######################################      Rondes     #####################################
@app.get("/rondes/", response_model=List[Ronda])
def get_rondes_all():
    return get_rondes()

######################################      Emparellaments      #####################################
@app.get("/emparellaments/", response_model=List[Emparellaments])
def get_emparellaments_all():
    return get_emparellaments()
#####################################      Usuaris       #####################################

@app.get("/users/", response_model=List[Usuaris])
def get_usuaris_all():
    return get_usuaris()


######################################  Tornejos  #####################################
@app.get("/tornejos/", response_model=List[Torneig])
def get_tornejos_all():
    return get_torneig()

#####################################  Get boolean rondes torneig acabades  #####################################
@app.get("/rondes/ronda_acabada", response_model=int)
def get_ronda_acabada(torneig_id: int):
    return get_ronda_acabada_id(torneig_id)
#####################################  Puntuacio Torneig #####################################

@app.get("/users/users_in_tournament", response_model=List[UserWithPoints])
def get_users_in_tournament(torneig_id: int):
    return get_users_points(torneig_id)


##################################### Get puntuacions Torneig per id  #####################################
@app.get("/puntuacions/get_by_tournament/{torneig_id}", response_model=List[Puntuacio])
def get_puntuacio_by_id(torneig_id: int):
    return get_puntuacio_id(torneig_id)

##################################### Get puntuacions Torneig per id ASC #####################################
@app.get("/puntuacions/get_by_tournament_ordered/{torneig_id}", response_model=List[Puntuacio])
def get_puntuacions_by_tournament_ordered(torneig_id: int):
    return get_putuacio_by_sos(torneig_id)

##################################### Get puntuacions Torneig per id ASC #####################################
@app.get("/puntuacions/get_by_tournament_ordered_and_name/{torneig_id}", response_model=List[PuntuacioName])
def get_puntuacions_by_tournament_orderedname(torneig_id: int):
    return get_putuacio_by_sosname(torneig_id)
##################################### Usuaris check nom  #####################################

@app.get("/users/check_username", response_model=bool)
def check_username_exists(username: str):
    return check_username(username)

##################################### Usuaris check nom  #####################################

@app.get("/users/check_mail", response_model=bool)
def check_mail_exists(email: str):
    return check_email_exists(email)

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

#####################################   New Pairing  #####################################
@app.get("/rondas/get_new_pairing", response_model=EmparellamentNom)
def get_ronda_by_torneig(torneig_id: int, usuari_id: int):
    return get_pairing_by_player_and_tournament(usuari_id, torneig_id)
#####################################   Tornejos Actius per ID   #####################################
@app.get("/tournaments/active_by_id", response_model=Torneig)
def get_active_tournament_by_id_endpoint(torneig_id: int):
    return get_active_tournament_by_id(torneig_id)

#####################################   Tornejos Actius   #####################################

@app.get("/tournaments/ended", response_model=List[Torneig])
def get_active_tournaments():
    return get_ended_tournaments_from_db()


#####################################   Tornejos Actius per ID   #####################################
@app.get("/tournaments/ended_by_id", response_model=Torneig)
def get_active_tournament_by_id_endpoint(torneig_id: int):
    return get_ended_tournament_by_id(torneig_id)


#####################################   Afegir Usuari    #####################################

@app.post("/users/add_user", response_model=Usuaris)
def add_user(user: NewUser):
    return add_usuari(user)


#####################################   Afegir Torneig   #####################################
@app.post("/tournaments/create", response_model=Torneig)
def create_tournament(tournament: NewTorneig):
    return add_tournament_to_db(tournament)

#####################################   Afegir Puntuacio   #####################################

@app.post("/puntuacions/add", response_model=Puntuacio)
def add_puntuacio(puntuacio: NewPuntuacio):
    try:
        return add_puntuacio_to_db(puntuacio)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
#####################################   Afegir Ronda     #####################################
@app.post("/rondes/add", response_model=Ronda)
def add_ronda(info_ronda: NewRonda):

    print("Received request body:", info_ronda)
    return add_ronda_to_db(info_ronda)
##################################### Usuaris update nom #####################################

@app.put("/users/update_name/{user_id}", response_model=Usuaris)
def update_user_name(user_id: int, update_name_request: UpdateNameRequest):
    username = update_name_request.username
    return update_username(user_id, username)

##################################### Usuaris update password #####################################
@app.put("/users/update_password", response_model=bool)
def update_password(passwordUpdateRequest: PasswordUpdateRequest):
    success = update_user_password_in_db(
        passwordUpdateRequest.email,
        passwordUpdateRequest.novaContrasenya
    )
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update password.")
    return success
##################################### Update ronda  #####################################
@app.put("/rondes/update_ronda", response_model=Ronda)
def update_ronda( update_ronda_request: UpdateRondaRequest):
    return update_ronda_to_db(update_ronda_request)
    
#################################### Delete Usuaris  #########################################
@app.delete("/users/delete_by_id/{user_id}", response_model=bool)
def delete_user_by_id(user_id: int):
    return delete_user_id(user_id)
    

##################################### Delete Puntuacions  #########################################
@app.delete("/puntuacions/delete_puntuacions_tournament/{torneig_id}")
def delete_puntuacions(torneig_id: int):
    return delete_puntuacions_by_tournament(torneig_id)

##################################### Delete Puntuacions  #########################################
@app.delete("/puntuacions/delete_by_user/{user_id}/{tournament_id}")
def delete_puntuacions_by_user_id(user_id: int, tournament_id: int):
    return delete_puntuacions_by_user(user_id, tournament_id)

##################################### Delete emparellaments i ronda  #########################################
@app.delete("/emparellaments/delete_emparellament_torneig/{torneig_id}")
def delete_emparellament_torneig(torneig_id: int):
    return delete_emparellament_torneig_id(torneig_id)

@app.get("/")
def read_docs():
    return read_docs()

@app.get("/docs")
def read_docs():
    return {"message": "This is the documentation endpoint."}
"""

##################################### GET METHODS #####################################



#####################################      FAST AP        #####################################

@app.get("/")
def read_docs():
    return read_docs()

@app.get("/docs")
def read_docs():
    return {"message": "This is the documentation endpoint."}





@app.get("/formats/", response_model=List[Format])
def get_formats_all():
    return get_formats()


@app.get("/rangs/", response_model=List[Rang])
def get_rangs_all():
    return get_rangs()

@app.get("/resultats/", response_model=List[Resultat])
def get_resultats_all():
    return get_resultats()

@app.get("/rols/", response_model=List[Rol])
def get_rols_all():
    return get_rols()

@app.get("/subscripcions/", response_model=List[Subscripcio])
def get_subscripcions_all():
    return get_subscripcions()

@app.get("/tornejos/", response_model=List[Torneig])
def get_tornejos_all():
    return get_torneig()


"""