import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_CONNECTION_STRING = os.getenv("DATABASE_CONNECTION_STRING")
engine = create_engine(DATABASE_CONNECTION_STRING)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
