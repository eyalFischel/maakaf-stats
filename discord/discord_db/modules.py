"""db table modules"""

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    """base class for the modules to inherit"""


class User(Base):
    """user table"""

    __tablename__: str = "users"

    user_id = mapped_column(String, primary_key=True)
    username = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        return f"user_id: {self.user_id} username: {self.username}"

class Member(Base):
    """member table"""

    __tablename__: str = "members"

    user_id = mapped_column(String, primary_key=True)
    guild_id = mapped_column(String, primary_key=True)
    joined_at = mapped_column(DateTime, nullable=False)

    def __repr__(self) -> str:
        return f"user_id: {self.user_id} guild_id: {self.guild_id} joined_at: {self.joined_at}"


class Guild(Base):
    """guild table"""

    __tablename__: str = "guilds"

    guild_id = mapped_column(String, primary_key=True)
    name = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        return f"guild_id: {self.guild_id} name: {self.name}"
    

class Channel(Base):
    """channel table"""

    __tablename__: str = "channels"

    channel_id = mapped_column(String, primary_key=True)
    guild_id = mapped_column(String, ForeignKey("guilds.guild_id"), nullable=False)
    name = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        return f"channel_id: {self.channel_id} guild_id: {self.guild_id} name: {self.name}"


class Message(Base):
    """message table"""

    __tablename__: str = "messages"

    message_id = mapped_column(String, primary_key=True)
    channel_id = mapped_column(
        String, ForeignKey("channels.channel_id"), nullable=False
    )
    guild_id = mapped_column(String, ForeignKey("guilds.guild_id"), nullable=False)
    user_id = mapped_column(String, nullable=False)
    created_at = mapped_column(DateTime, nullable=False)

    def __repr__(self) -> str:
        return f"\
        message_id: {self.message_id} \
        channel_id: {self.channel_id} \
        guild_id: {self.guild_id} \
        user_id: {self.user_id} \
        timestamp: {self.created_at}\
        "
