"""configure and create the database"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .logger import Logger
from .modules import Base

load_dotenv()

DB_URL: str = os.getenv("DB_URL")

try:
    engine = create_engine(DB_URL)

    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
except Exception as e:
    Logger.error(f"Error connecting to database: {e}")
    raise
