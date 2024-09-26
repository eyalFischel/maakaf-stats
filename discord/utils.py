"""helper functions for the discord bot"""

from datetime import datetime

from sqlalchemy import select

from discord_db.modules import Guild, Channel, Message, Member


def insert_user(session, user_id: str, guild_id: str, joined_at: datetime) -> None:
    """insers a user to the db"""
    stmt = select(Member).where(Member.user_id == user_id and Member.guild_id == guild_id)
    if session.scalars(stmt).first():
        return

    user = Member(user_id=user_id, guild_id=guild_id, joined_at=joined_at)
    session.add(user)
    session.commit()

def insert_update_guild(session, guild_id: str, name: str):
    """inserts a guild to the db"""
    stmt = select(Guild).where(Guild.guild_id == guild_id)
    guild = session.scalars(stmt).first()
    if guild:
        if guild.name != name:
            guild.name = name
            session.commit()
        return
    
    guild = Guild(guild_id=guild_id, name=name)
    session.add(guild)
    session.commit()


def insert_update_channel(session, channel_id: str, guild_id: str, name: str) -> None:
    """inserts a channel to the db"""
    stmt = select(Channel).where(Channel.channel_id == channel_id)
    channel = session.scalars(stmt).first()
    if channel:
        if channel.name != name:
            channel.name = name
            session.commit()
        return

    channel = Channel(channel_id=channel_id, guild_id=guild_id, name=name)
    session.add(channel)
    session.commit()


def insert_message(
    session, message_id: str, channel_id: str, guild_id: str, user_id: str, created_at: datetime
) -> None:
    """inserts a message to the db"""
    stmt = select(Message).where(Message.message_id == message_id)
    if session.scalars(stmt).first():
        return

    message = Message(
        message_id=message_id,
        channel_id=channel_id,
        guild_id=guild_id,
        user_id=user_id,
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
