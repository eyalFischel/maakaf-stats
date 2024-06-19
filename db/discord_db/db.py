from base import Base
from user import User
from channel import Channel
from message import Message

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()

DB_URL: str = os.getenv('PG_DATABASE_URL')

engine = create_engine(DB_URL)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)