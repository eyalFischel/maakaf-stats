from base import Base

from sqlalchemy import String
from sqlalchemy.orm import mapped_column

class Channel(Base):
    __tablename__: str = 'channels'

    channel_id = mapped_column(String, primary_key=True)
    name = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        return f'channel_id: {self.channel_id} name: {self.name}'