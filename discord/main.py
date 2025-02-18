"""discord bot that tracks guild member activity and save it on db"""

from datetime import timedelta, datetime
import os

from dotenv import load_dotenv
import discord

from discord_db.db import Session
from discord_db.logger import Logger
from utils import (
    insert_update_guild,
    insert_update_channel,
    insert_message,
    insert_member,
    get_channel_latest_message,
    insert_update_user,
    insert_reaction,
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

                for member in guild.members:
                    try:
                        insert_member(
                            session,
                            str(member.id),
                            guild_id,
                            member.joined_at,
                            member.name,
                        )
                    except Exception as e:
                        Logger.error(f"Error inserting user {member.id}: {e}")

                for channel in guild.text_channels:
                    channel_id = str(channel.id)
                    try:
                        insert_update_channel(
                            session, channel_id, guild_id, channel.name
                        )
                    except Exception as e:
                        Logger.error(f"Error inserting channel {channel.name}: {e}")

                    try:
                        last_message_in_db = get_channel_latest_message(
                            session, channel_id
                        )
                        last_message_time_in_db = None
                        if last_message_in_db:
                            last_message_time_in_db = (
                                last_message_in_db.created_at
                                - timedelta(milliseconds=1)
                            )
                    except Exception as e:
                        Logger.error(
                            f"Error fetching latest message for channel {channel.name}: {e}"
                        )

                    try:
                        async for message in channel.history(
                            limit=None, after=last_message_time_in_db
                        ):
                            if message.author.bot:
                                continue
                            try:
                                insert_message(
                                    session,
                                    str(message.id),
                                    channel_id,
                                    guild_id,
                                    str(message.author.id),
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
            session.commit()

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
                    str(message.author.id),
                    message.created_at,
                )
            except Exception as e:
                Logger.error(
                    f"Error inserting message {message.id} from channel {message.channel.id}: {e}"
                )
            session.commit()

    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel) -> None:
        """adds the new guild channel to the db"""
        with Session() as session:
            try:
                insert_update_channel(
                    session, str(channel.id), str(channel.guild.id), channel.name
                )
            except Exception as e:
                Logger.error(f"Error inserting channel {channel.name}: {e}")
            session.commit()

    async def on_member_join(self, member: discord.member) -> None:
        """adds the new member to the db"""
        with Session() as session:
            try:
                insert_member(
                    session,
                    str(member.id),
                    str(member.guild.id),
                    member.joined_at,
                    member.name,
                )
            except Exception as e:
                Logger.error(
                    f"Error inserting member {member.id} from guild {member.guild.id}: {e}"
                )
            session.commit()

    async def on_guild_join(self, guild) -> None:
        """adds the new joined guild to the db"""
        with Session() as session:
            try:
                insert_update_guild(session, str(guild.id), guild.name)
            except Exception as e:
                Logger.error(f"Error inserting guild {guild.name}: {e}")
            session.commit()

    async def on_guild_channel_update(self, before, after) -> None:
        """updates the channel changes in the db"""
        if before.name != after.name:
            with Session() as session:
                try:
                    insert_update_channel(
                        session, str(after.id), str(after.guild.id), after.name
                    )
                except Exception as e:
                    Logger.error(f"Error updating name of channel {before.name}: {e}")
                session.commit()

    async def on_guild_update(self, before, after) -> None:
        """updates the guild changes in the db"""
        if before.name != after.name:
            with Session() as session:
                try:
                    insert_update_guild(session, str(after.id), after.name)
                except Exception as e:
                    Logger.error(f"Error updating name of guild {before.name}: {e}")
                session.commit()

    async def on_user_update(self, before, after) -> None:
        """updates the user changes in the db"""
        if before.name != after.name:
            with Session() as session:
                try:
                    insert_update_user(session, str(after.id), after.name)
                except Exception as e:
                    Logger.error(f"Error updating username of user {before.id}: {e}")
                session.commit()

    async def on_raw_reaction_add(self, payload) -> None:
        """add the reaction to db"""
        if payload.emoji.id:
            emoji_id: str = str(payload.emoji.id)
        else:
            emoji_id: str = payload.emoji.name
        message_id: str = str(payload.message_id)
        user_id: str = str(payload.user_id)
        channel_id: str = str(payload.channel_id)
        guild_id: str = str(payload.guild_id)
        added_at: datetime = datetime.now()

        with Session() as session:
            try:
                insert_reaction(
                    session,
                    emoji_id,
                    message_id,
                    user_id,
                    channel_id,
                    guild_id,
                    added_at,
                )
            except Exception as e:
                Logger.error(
                    f"Error inserting reaction of emoji {emoji_id} for message {message_id} from user {user_id}: {e}"
                )
            session.commit()


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.members = True
    client = DiscordBot(intents=intents)
    try:
        client.run(BOT_TOKEN)
    except Exception as e:
        Logger.error(f"Error starting the bot: {e}")
