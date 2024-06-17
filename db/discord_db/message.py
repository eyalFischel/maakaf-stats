from db.discord_db.db import Base

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column

class Message(Base):
    __tablename__: str = 'messages'

    message_id = mapped_column(String, primary_key=True)
    channel_id = mapped_column(String, ForeignKey('channels.channel_id'), nullable=False)
    username = mapped_column(String, ForeignKey('users.username'), nullable=False)

    def __repr__(self) -> str:
        return f'message_id: {self.message_id} channel_id: {self.channel_id} username: {self.username}'