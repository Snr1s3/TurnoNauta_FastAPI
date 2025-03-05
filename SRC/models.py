from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class Emparellaments(BaseModel):
    id_emperallent: Optional[int]
    id_usuari1: int
    resultat_usuari_1: Optional[str]
    id_usuari2: int
    resultat_usuari_2: Optional[str]

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
    id_puntuacio: Optional[int]
    id_torneig: int
    id_usuari: int
    victories: Optional[int]
    derrotes: Optional[int]
    punts: Optional[int]

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
    id_emparallent: Optional[int]

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
    data_d_inici: date
    data_final: Optional[date]

class Usuaris(BaseModel):
    id_usuaris: Optional[int]
    rol: Optional[int]
    username: str
    email: str
    bio: Optional[str]
    telefono: Optional[str]
    contrasenya: str
    rang: Optional[int]
    data_de_registre: Optional[date]