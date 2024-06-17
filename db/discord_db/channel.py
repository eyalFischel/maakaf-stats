from base import Base

from sqlalchemy import Column, String

class Channel(Base):
    __tablename__ = 'channels'

    channel_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f'channel_id: {self.channel_id} name: {self.name}'