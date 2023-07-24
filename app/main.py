from fastapi import FastAPI
from fastapi.params import Depends
from typing import List
from starlette.responses import RedirectResponse
from . import models, schemas
from .connect import SessionLocal, engine

from sqlalchemy import Date, cast, func
from sqlalchemy.orm import Session
from datetime import date

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def main():
    return RedirectResponse(url="/docs")

@app.get("/games/", response_model=List[schemas.Game])
def get_games(db:Session=Depends(get_db)):         
    response = db.query(models.Game).all()
    return response

@app.get("/games/{game_id}/", response_model=schemas.Game)
def get_game_by_id(game_id:int, db:Session=Depends(get_db)):
    response = db.query(models.Game).filter_by(id=game_id).first()
    return response

@app.get("/games/{game_id}/soundtracks", response_model=List[schemas.Soundtrack])
def get_game_soundtracks(game_id:int, db:Session=Depends(get_db)):

    response = db.query(models.Soundtrack).filter_by(game_id = game_id).all()
    return response


@app.get("/soundtracks/", response_model=List[schemas.Soundtrack])
def get_soundtracks(db:Session=Depends(get_db)):

    response = db.query(models.Soundtrack).all()

    return response

#@app.get("/ostdlegame/", response_model= List[schemas.OstdleGame]) ERROR ON THE SCHEMA
@app.get("/ostdlegame/")
def get_ostdlegames(db:Session=Depends(get_db)):

    response = db.query(models.OstdleGame).all()

    return response

@app.get("/ostdlegame/{game_id}")
def get_ostdlegame_by_id(game_id:int, db:Session=Depends(get_db)):

    response = db.query(models.OstdleGame, models.Soundtrack, models.Game).filter(
        models.OstdleGame.id == game_id).join(
        models.Soundtrack, models.Soundtrack.id == models.OstdleGame.soundtrack_id).join(
        models.Game, models.Game.id == models.Soundtrack.game_id).first()
    
    return response

@app.get("/today/")
def get_today(db:Session = Depends(get_db)):

    tdy_game = db.query(models.OstdleGame).filter(
        cast(models.OstdleGame.date, Date) == date.today()
        ).first()

    # Create game for today if doesn't exists
    if(tdy_game == None):
        id = create_today_game(db)
    else:
        id = tdy_game.id

    tdy_game = db.query(models.OstdleGame, models.Soundtrack, models.Game).filter(
        models.OstdleGame.id == id).join(
        models.Soundtrack, models.Soundtrack.id == models.OstdleGame.soundtrack_id).join(
        models.Game, models.Game.id == models.Soundtrack.game_id).first()
    
    return tdy_game

# Create game for today
def create_today_game(db):

    soundtrack = db.query(models.Soundtrack).filter_by(played = False).order_by(func.random()).first()
    soundtrack.played = True

    print(soundtrack.id)

    new_gameOstdle = models.OstdleGame(date = date.today(), soundtrack_id = soundtrack.id)

    db.add(new_gameOstdle)
    db.commit()

    db.refresh(soundtrack)
    db.refresh(new_gameOstdle)

    return(new_gameOstdle.id)