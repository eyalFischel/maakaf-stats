from sqlalchemy import String, DateTime, ARRAY, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__: str = 'users'

    username = mapped_column(String, primary_key=True)
    joined_at = mapped_column(DateTime, nullable=False)
    # roles = mapped_column(ARRAY(String), nullable=False)

    def __repr__(self) -> str:
        return f'username: {self.username} joined_at: {self.joined_at}'
    

class Channel(Base):
    __tablename__: str = 'channels'

    channel_id = mapped_column(String, primary_key=True)
    name = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        return f'channel_id: {self.channel_id} name: {self.name}'
    
class Message(Base):
    __tablename__: str = 'messages'

    message_id = mapped_column(String, primary_key=True)
    channel_id = mapped_column(String, ForeignKey('channels.channel_id'), nullable=False)
    username = mapped_column(String, ForeignKey('users.username'), nullable=False)
    created_at = mapped_column(DateTime, nullable=False)

    def __repr__(self) -> str:
        return f'message_id: {self.message_id} channel_id: {self.channel_id} username: {self.username} timestamp: {self.create_at}'