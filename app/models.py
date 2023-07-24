from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .connect import Base

class Game(Base):
    __tablename__='game'
    id = Column(Integer, primary_key = True, index=True)
    name = Column(String(80))
    franchise = Column(String(50))

class Soundtrack(Base):
    __tablename__ ='soundtrack'
    id = Column(Integer, primary_key = True, index=True)
    name = Column(String(80))
    src = Column(String(80))
    played = Column(Boolean, default=False)

    game_id = Column(Integer, ForeignKey('game.id'))
    game = relationship('Game', foreign_keys=[game_id])


class OstdleGame(Base):
    __tablename__='ostdle_game'
    id = Column(Integer, primary_key = True, index=True)
    date = Column(Date)

    soundtrack_id = Column(Integer, ForeignKey('soundtrack.id'))
    soundtrack = relationship('Soundtrack', foreign_keys=[soundtrack_id])    
