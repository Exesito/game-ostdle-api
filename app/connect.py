from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ

database_url = environ['DATABASE_URL']

database_url = database_url.replace('postgres://', 'postgresql://')

engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()