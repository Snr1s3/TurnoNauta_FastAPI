from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class Emparellaments(BaseModel):
    ID_Emparellament: Optional[int]
    Usuari1: int
    Usuari2: int

class Estadistiques(BaseModel):
    ID_Estats: Optional[int]
    Partides_jugades: Optional[int] = 0
    Partides_guanyades: Optional[int] = 0
    Torneigs_jugats: Optional[int] = 0
    Torneigs_guanyats: Optional[int] = 0

class Format(BaseModel):
    ID_Format: Optional[int]
    Nom: str
    Joc: str
    Jugadors: int
    Temps: Optional[str]
    Regles: Optional[str]

class Jugadors(BaseModel):
    ID_Jugador: Optional[int]
    ID_Torneig: int
    ID_Usuari: int

class Puntuacio(BaseModel):
    ID_Puntuacio: Optional[int]
    ID_Torneig: int
    ID_Usuari: int
    Punts: int

class Rang(BaseModel):
    ID_Rang: Optional[int]
    Nom: str
    Descripcio: Optional[str]

class Resultat(BaseModel):
    ID_Resultat: Optional[int]
    ID_Ronda: int
    Usuari_Guanyador: Optional[int]
    ID_Joc_Torneig: int

class Ronda(BaseModel):
    ID_ronda: Optional[int]
    Estat: str
    ID_Emparellament: Optional[int]
    Numero_de_Ronda: int

class Rondes_Torneig(BaseModel):
    ID_Torneig: int
    ID_Ronda: int

class Rol(BaseModel):
    Id_Rol: Optional[int]
    Nom: str
    Permet_Torneig: bool

class Subscripcio(BaseModel):
    ID_Subcripcio: Optional[int]
    Data_inici: date
    Data_final: date
    Tipus: str
    Estat: str

class Torneig(BaseModel):
    ID: Optional[int]
    Nom: str
    Joc: str
    Usuari_Organitzador: int
    Competitiu: bool
    Virtual: bool
    Format: Optional[int]
    Premi: Optional[str]
    Data_Inici: date
    Data_Final: Optional[date]

class Usuaris(BaseModel):
    ID: Optional[int]
    Rol: Optional[int]
    Username: str
    Email: str
    Bio: Optional[str]
    Telefono: Optional[str]
    Contrasenya: str
    Subcripcio: Optional[int]
    Estadistiques: Optional[int]
    Rang: Optional[int]
    Data_de_Registre: Optional[datetime]