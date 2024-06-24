# import asyncio
# from datetime import datetime, timedelta
import os

import discord
from dotenv import load_dotenv

from utils import *
from discord_db.modules import *
from discord_db.db import Session

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

class DiscordBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.join_count: int = 0
        # # key: channel_name, value: [message_count, last_message_time] 
        # self.project_activity: dict[str,list] = {}
        # # key: member_name, value: {key: channel_name, val: [message_count, last_message_time]}
        # self.member_activity: dict[str,dict[str,list]] = {}


    async def on_ready(self) -> None:
        print(f"We have logged in as {client.user}")

        # asyncio.create_task(self.reset_counters_weekly())


    async def on_message(self, message: discord.message) -> None:
        if message.author.bot or message.channel.type.value != 0:
            return
        
        with Session() as session:
            insert_message(session, message.id, message.channel.id, message.author.name, message.created_at)
        # update_member_activity(message, self.member_activity)
        # if message.channel.category and is_projects_category(message.channel.category):
        #     update_project_activity(message, self.project_activity)


    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel) -> None:
            with Session() as session:
                insert_channel(session, channel.id, channel.name)


    async def on_member_join(self, member: discord.member) -> None:
        with Session() as session:
            insert_user(session, member.name, member.joined_at)
        # self.join_count += 1
        # print(member.name + " joined. " + f"{self.join_count} new members has joined this week")


    # async def reset_counters_weekly(self) -> None:
    #     await client.wait_until_ready()
    #     while not client.is_closed():
    #         now = datetime.now()
    #         days_until_next_sunday = (6 - now.weekday()) if now.weekday() != 6 else 7
    #         next_reset = now + timedelta(days=days_until_next_sunday)
    #         next_reset = next_reset.replace(hour=0, minute=0, second=0, microsecond=0)
    #         wait_time = (next_reset - now).total_seconds()

    #         print(f"next counters reset: {next_reset}")
    #         await asyncio.sleep(wait_time)

    #         self.join_count = 0

    #         print("Weekly counter reset " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    #         await asyncio.sleep(7*24*60*60)

if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.members = True
    client = DiscordBot(intents=intents)
    client.run(BOT_TOKEN)