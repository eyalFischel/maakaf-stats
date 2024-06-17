from base import Base

from sqlalchemy import Column, String

class channel(Base):
    __tablename__ = 'channels'

    channel_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f'channel_id: {self.channel_id} name: {self.name}'