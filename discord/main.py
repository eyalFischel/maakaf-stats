"""discord bot that tracks guild member activity and save it on db"""

import os

import discord
from dotenv import load_dotenv

from discord_db.db import Session
from discord_db.logger import Logger
from utils import (
    insert_update_guild,
    insert_update_channel,
    insert_message,
    insert_user,
    get_channel_latest_message,
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


class DiscordBot(discord.Client):
    """class for the discord"""

    async def on_ready(self) -> None:
        """
        called when the bot starts running,
        scans the db and updates the data
        """
        Logger.info(f"Bot is up as {self.user}")

        with Session() as session:
            for guild in self.guilds:
                guild_id = str(guild.id)
                try:
                    insert_update_guild(session, guild_id, guild.name)
                except Exception as e:
                    Logger.error(f"Error inserting guild {guild.name}: {e}")

                for user in guild.members:
                    try:
                        insert_user(session, user.name, guild_id, user.joined_at)
                    except Exception as e:
                        Logger.error(f"Error inserting user {user.name}: {e}")

                for channel in guild.text_channels:
                    channel_id = str(channel.id)
                    try:
                        insert_update_channel(session, channel_id, guild_id, channel.name)
                    except Exception as e:
                        Logger.error(f"Error inserting channel {channel.name}: {e}")

                    try:
                        last_message_in_db = get_channel_latest_message(
                            session, channel_id
                        )
                        if last_message_in_db:
                            last_message_in_db = await channel.fetch_message(
                                int(last_message_in_db.message_id)
                            )
                    except Exception as e:
                        Logger.error(
                            f"Error fetching latest message for channel {channel.name}: {e}"
                        )
                        last_message_in_db = None

                    try:
                        async for message in channel.history(
                            limit=None, after=last_message_in_db
                        ):
                            if message.author.bot:
                                continue
                            try:
                                insert_message(
                                    session,
                                    str(message.id),
                                    channel_id,
                                    guild_id,
                                    message.author.name,
                                    message.created_at,
                                )
                            except Exception as e:
                                Logger.error(
                                    f"Error inserting message {message.id} from channel {channel_id}: {e}"
                                )

                    except Exception as e:
                        Logger.error(
                            f"Failed to fetch messages from channel {channel.name}: {e}"
                        )

    async def on_message(self, message: discord.message) -> None:
        """adds the message info to the db"""
        if message.author.bot or message.channel.type.value != 0:
            return

        with Session() as session:
            try:
                insert_message(
                    session,
                    str(message.id),
                    str(message.channel.id),
                    str(message.guild.id),
                    message.author.name,
                    message.created_at,
                )
            except Exception as e:
                Logger.error(
                    f"Error inserting message {message.id} from channel {message.channel.id}: {e}"
                )

    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel) -> None:
        """adds the new guild channel to the db"""
        with Session() as session:
            try:
                insert_update_channel(session, str(channel.id), str(channel.guild.id), channel.name)
            except Exception as e:
                Logger.error(f"Error inserting channel {channel.name}: {e}")

    async def on_member_join(self, member: discord.member) -> None:
        """adds the new member to the db"""
        with Session() as session:
            try:
                insert_user(session, member.name, str(member.guild.id), member.joined_at)
            except Exception as e:
                Logger.error(f"Error inserting user {member.name} from guild {member.guild.id}: {e}")
    
    async def on_guild_join(self, guild) -> None:
        """adds the new joined guild to the db"""
        with Session as session:
            try:
                insert_update_guild(session, str(guild.id), guild.name)
            except:
                Logger.error(f"Error inserting guild {guild.name}: {e}")

    async def on_guild_channel_update(self, before, after) -> None:
        """updates the channel changes in the db"""
        if before.name != after.name:
            with Session() as session:
                try:
                    insert_update_channel(session, str(after.id), after.guild.id, after.name)
                except Exception as e:
                    Logger.error(f"Error updating name of channel {before.name}: {e}")
    
    async def on_guild_update(self, before, after) -> None:
        """updates the guild changes in the db"""
        if before.name != after.name:
            with Session() as session:
                try:
                    insert_update_guild(session, str(after.id), after.name)
                except Exception as e:
                    Logger.error(f"Error updating name of guild {before.name}: {e}")


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.members = True
    client = DiscordBot(intents=intents)
    try:
        client.run(BOT_TOKEN)
    except Exception as e:
        Logger.error(f"Error starting the bot: {e}")
