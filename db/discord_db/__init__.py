from base import Base, engine
from user import User
from channel import Channel
from message import Message


Base.metadata.create_all(bind=engine)