import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()

DB_URL = os.getenv('PG_DATABASE_URL')

engine = create_engine(DB_URL)

Base = declarative_base()

Session = sessionmaker(bind=engine)