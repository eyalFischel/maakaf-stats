"""discord bot that tracks guild member activity and save it on db"""

import os

import discord
from dotenv import load_dotenv

from discord_db.db import Session
from utils import insert_user, insert_channel, insert_message, update_channel

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


class DiscordBot(discord.Client):
    """class for the discord"""

    async def on_ready(self) -> None:
        """
        called when the bot starts running,
        scans the db and updates the data
        """
        print(f"We have logged in as {client.user}")

        with Session() as session:
            for user in client.guilds[0].members:
                insert_user(session, user.name, user.joined_at)
            for channel in client.guilds[0].text_channels:
                insert_channel(session, str(channel.id), channel.name)
                async for message in channel.history(limit=None):
                    if message.author.bot:
                        continue
                    insert_message(
                        session,
                        str(message.id),
                        str(message.channel.id),
                        message.author.name,
                        message.created_at,
                    )

    async def on_message(self, message: discord.message) -> None:
        """adds the message info to the db"""
        if message.author.bot or message.channel.type.value != 0:
            return

        with Session() as session:
            insert_message(
                session,
                str(message.id),
                str(message.channel.id),
                message.author.name,
                message.created_at,
            )

    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel) -> None:
        """adds the new guild channel to the db"""
        with Session() as session:
            insert_channel(session, str(channel.id), channel.name)

    async def on_member_join(self, member: discord.member) -> None:
        """adds the new member to the db"""
        with Session() as session:
            insert_user(session, member.name, member.joined_at)

    async def on_guild_channel_update(self, before, after) -> None:
        """updates the channel changes in the db"""
        if before.name != after.name:
            with Session() as session:
                update_channel(session, str(after.id), after.name)


intents = discord.Intents.default()
intents.members = True
client = DiscordBot(intents=intents)
client.run(BOT_TOKEN)
