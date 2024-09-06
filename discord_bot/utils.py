"""helper functions for the discord bot"""

from datetime import datetime

from sqlalchemy import select

from discord_db.modules import Channel, Message, User


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


def get_channel_latest_message(session, channel_id: str) -> Message:
    """get the latest message in the db"""
    stmt = (
        select(Message)
        .where(Message.channel_id == channel_id)
        .order_by(Message.created_at.desc())
    )
    last_message = session.scalars(stmt).first()
    return last_message


def update_channel(session, channel_id: str, name: str) -> None:
    """update a channel in the db"""
    stmt = select(Channel).where(Channel.channel_id == channel_id)
    channel = session.scalars(stmt).first()
    channel.name = name
    session.commit()
