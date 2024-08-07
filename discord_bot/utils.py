"""helper functions for the discord bot"""

from datetime import datetime

from discord_db.modules import Channel, Message, User
from sqlalchemy import select


def insert_user(session, username: str, joined_at: datetime) -> None:
    """insers a user to the db"""
    stmt = select(User).where(User.username == username)
    if session.scalars(stmt).first():
        return

    user = User(username=username, joined_at=joined_at)
    session.add(user)
    session.commit()


def insert_channel(session, channel_id: str, name: str) -> None:
    """inserts a channel to the db"""
    stmt = select(Channel).where(Channel.channel_id == channel_id)
    channel = session.scalars(stmt).first()
    if channel:
        if channel.name != name:
            channel.name = name
            session.commit()
        return

    channel = Channel(channel_id=channel_id, name=name)
    session.add(channel)
    session.commit()


def insert_message(
    session, message_id: str, channel_id: str, username: str, created_at: datetime
) -> None:
    """inserts a message to the db"""
    stmt = select(Message).where(Message.message_id == message_id)
    if session.scalars(stmt).first():
        return

    message = Message(
        message_id=message_id,
        channel_id=channel_id,
        username=username,
        created_at=created_at,
    )
    session.add(message)
    session.commit()


def update_channel(session, channel_id: str, name: str) -> None:
    """update a channel in the db"""
    stmt = select(Channel).where(Channel.channel_id == channel_id)
    channel = session.scalars(stmt).first()
    channel.name = name
    session.commit()
