"""configure and create the database"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .modules import Base

load_dotenv()

DB_URL: str = os.getenv("PG_DATABASE_URL")

engine = create_engine(DB_URL)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
