"""db table modules"""

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    """base class for the modules to inherit"""


class User(Base):
    """user table"""

    __tablename__: str = "users"

    username = mapped_column(String, primary_key=True)
    joined_at = mapped_column(DateTime, nullable=False)

    def __repr__(self) -> str:
        return f"username: {self.username} joined_at: {self.joined_at}"


class Channel(Base):
    """channel table"""

    __tablename__: str = "channels"

    channel_id = mapped_column(String, primary_key=True)
    name = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        return f"channel_id: {self.channel_id} name: {self.name}"


class Message(Base):
    """message table"""

    __tablename__: str = "messages"

    message_id = mapped_column(String, primary_key=True)
    channel_id = mapped_column(
        String, ForeignKey("channels.channel_id"), nullable=False
    )
    username = mapped_column(String, nullable=False)
    created_at = mapped_column(DateTime, nullable=False)

    def __repr__(self) -> str:
        return f"\
        message_id: {self.message_id} \
        channel_id: {self.channel_id} \
        username: {self.username} \
        timestamp: {self.created_at}\
        "
