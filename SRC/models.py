from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class Emparellaments(BaseModel):
    id_emperallent: Optional[int]
    id_ronda: Optional[int]
    id_usuari1: int
    resultat_usuari_1: int
    id_usuari2: int
    resultat_usuari_2: int
    id_usuari_guanyador: Optional[int]
    id_usuari_perdedor: Optional[int]

class EmparellamentNom(BaseModel):
    id_emperallent: Optional[int]
    id_ronda: Optional[int]
    nom_usuari1: str
    id_usuari1: int
    resultat_usuari_1: int
    nom_usuari2: str
    id_usuari2: int
    resultat_usuari_2: int
    id_usuari_guanyador: Optional[int]
    id_usuari_perdedor: Optional[int]

class Estadistiques(BaseModel):
    id_estats: Optional[int]
    id_usuari: int
    partides_jugades: Optional[int] = 0
    partides_guanyades: Optional[int] = 0
    tornejos_jugats: Optional[int] = 0
    tornejos_guanyats: Optional[int] = 0

class Format(BaseModel):
    id_format: Optional[int]
    nom: str
    joc: str
    jugadors: int
    temps: Optional[str]
    regles: Optional[str]

class Puntuacio(BaseModel):
    id_torneig: int
    id_usuari: int
    sos: int
    victories: int
    empat: int
    derrotes: int
    punts: int

class Rang(BaseModel):
    id_rang: Optional[int]
    nom: str
    descripcio: Optional[str]

class Resultat(BaseModel):
    id_resultat: Optional[int]
    id_ronda: int
    id_usuari_guanyador: Optional[int]

class Rol(BaseModel):
    id_rol: Optional[int]
    nom: str
    permet_torneig: bool

class Ronda(BaseModel):
    id_ronda: Optional[int]
    id_torneig: int
    estat: str

class Subscripcio(BaseModel):
    id_subscripcio: Optional[int]
    id_usuari: int
    data_inici: date
    data_final: Optional[date]
    tipus: str
    estat: str

class Torneig(BaseModel):
    id_torneig: Optional[int]
    nom: str
    joc: str
    usuari_organitzador: int
    competitiu: bool
    virtual: bool
    format: Optional[str]
    premi: Optional[str]
    num_jugadors: Optional[int]
    data_d_inici: date
    data_final: Optional[date]

class NewTorneig(BaseModel):
    nom: str
    joc: str
    usuari_organitzador: int
    competitiu: bool
    virtual: bool
    format: Optional[str]
    premi: Optional[str]
    num_jugadors: Optional[int]
    data_d_inici: date
    data_final: Optional[date]

class Usuaris(BaseModel):
    id_usuaris: int
    rol: Optional[int]
    username: str
    email: str
    bio: Optional[str]
    telefono: Optional[str]  
    contrasenya: str
    rang: Optional[int]
    data_de_registre: Optional[date]

class UserStatistics(BaseModel):
    id: int
    username: str
    rounds_played: int
    rounds_won: int
    tournaments_played: int
    tournaments_won: int

class UserWithPoints(BaseModel):
    username: str
    punts: int

class NewUser(BaseModel):
    username: str
    email: str
    phone: str
    password: str

class UpdateNameRequest(BaseModel):
    username: str

class NewPuntuacio(BaseModel):
    id_torneig: int
    id_usuari: int
    sos: int
    victories: int
    empat: int
    derrotes: int
    punts: int

class NewRonda(BaseModel):
    id_torneig: int
    id_player1: int
    id_player2: int

class UpdateRondaRequest(BaseModel):
    id_ronda: int
    id_usuari_1: int
    resultat_usuari_1: int
    id_usuari_2: int
    resultat_usuari_2: int
    id_usuari_guanyador: int
    id_usuari_perdedor: int