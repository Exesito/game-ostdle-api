from typing import Optional, Tuple, List
from pydantic import BaseModel
from datetime import date


class Game(BaseModel):

    id: Optional[int] = 0
    name: Optional[str] = None
    franchise: Optional[str] = None

    class Config:
        orm_mode = True

class OstdleGame(BaseModel):
    id: int
    game_date: date
    soundtrack_id: int
    

class Soundtrack(BaseModel):
    id: Optional[int] = 0
    name:str
    src:str
    game_id: int

    class Config:
        orm_mode = True

class SoundtrackWithGame(BaseModel):
    Soundtrack: Soundtrack
    Game: Game

class DetailsOstdleGame(BaseModel):

    OstdleGame: OstdleGame
    Soundtrack: Soundtrack
    Game: Game
