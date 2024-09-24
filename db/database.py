import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, engine

load_dotenv()

database = create_engine("sqlite:///notes.db", connect_args={"check_same_thread": False})
Session = sessionmaker(bind=database)
session = Session()
Base = declarative_base()



def create_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()









