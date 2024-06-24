from datetime import datetime

import discord
from sqlalchemy import select


from discord_db.modules import *
# from db.discord_db.db import Session

def insert_user(session, username: str, joined_at: datetime) -> None:
    stmt = select(User).where(User.username==username)
    if session.scalars(stmt).first():
        return
    
    user = User(username=username, joined_at=joined_at)
    session.add(user)
    session.commit()

def insert_channel(session, channel_id: str, name: str) -> None:
    stmt = select(Channel).where(Channel.channel_id==channel_id)
    if session.scalars(stmt).first():
        return
    
    channel = Channel(channel_id=channel_id, name=name)
    session.add(channel)
    session.commit()

def insert_message(session, message_id: str, channel_id: str, username: str, created_at: datetime) -> None:
    message = Message(message_id=message_id, channel_id=channel_id, username=username, created_at=created_at)
    session.add(message)
    session.commit()

def is_projects_category(category: discord.CategoryChannel) -> bool:
    return category.name.lower().startswith('projects-')

def is_text_channel(channel: discord.channel) -> bool:
    return channel.type.value == 0

def update_member_activity(message: discord.message, member_activity: dict[str,dict[str,list]]) -> None:
    author = message.author
    channel = message.channel

    if author.name not in member_activity:
        member_activity[author.name] = {}
    
    if channel.name not in member_activity[author.name]:
        member_activity[author.name][channel.name] = [0, 0]
    
    member_activity[author.name][channel.name][0] += 1
    member_activity[author.name][channel.name][1] = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
    print(f'member activity: {member_activity}')

def update_project_activity(message: discord.message, project_activity: dict[str,list]) -> None:
    channel_name: str = message.channel.name
    created_at = message.created_at

    if channel_name not in project_activity:
        project_activity[channel_name] = [0, 0]
    
    project_activity[channel_name][0] += 1
    project_activity[channel_name][1] = created_at.strftime('%Y-%m-%d %H:%M:%S')
    print(f'project activity: {project_activity}')
