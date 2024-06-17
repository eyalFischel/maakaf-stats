from base import Base

from sqlalchemy import Column, String, ForeignKey

class Message(Base):
    __tablename__ = 'messages'

    message_id = Column(String, primary_key=True)
    channel_id = Column(String, ForeignKey('channels.channel_id'), nullable=False)
    username = Column(String, ForeignKey('users.username'), nullable=False)

    def __repr__(self) -> str:
        return f'message_id: {self.message_id} channel_id: {self.channel_id} username: {self.username}'