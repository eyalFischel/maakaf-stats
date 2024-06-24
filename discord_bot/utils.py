"""helper functions for the discord bot"""

from datetime import datetime

from sqlalchemy import select


from discord_db.modules import User, Channel, Message


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
    if session.scalars(stmt).first():
        return

    channel = Channel(channel_id=channel_id, name=name)
    session.add(channel)
    session.commit()


def insert_message(
    session, message_id: str, channel_id: str, username: str, created_at: datetime
) -> None:
    """inserts a message to the db"""
    message = Message(
        message_id=message_id,
        channel_id=channel_id,
        username=username,
        created_at=created_at,
    )
    session.add(message)
    session.commit()
