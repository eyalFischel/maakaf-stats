import asyncio
from datetime import datetime, timedelta
import discord
from dotenv import load_dotenv
import os
from utils import *

intents = discord.Intents.default()
intents.members = True

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

client = discord.Client(intents=intents)

join_count = 0

# key: channel_name, value: [message_count, last_message_time] 
project_activity = {}
# key: member_name, value: {key: channel_name, val: [message_count, last_message_time]}
member_activity = {}

@client.event
async def on_ready() -> None:
    print(f"We have logged in as {client.user}")

    asyncio.create_task(reset_counters_weekly())


@client.event
async def on_message(message):
    if message.author.bot:
        return
    
    update_member_activity(message, member_activity)
    if message.channel.category and is_projects_category(message.channel.category):
        update_project_activity(message, project_activity)

    
@client.event
async def on_member_join(member):
    if member.guild.id == GUILD_ID:
        global join_count
        join_count += 1
        print(member.name + " joined. " + f"{join_count} new members has joined this week")


async def reset_counters_weekly() -> None:
    await client.wait_until_ready()
    while not client.is_closed():
        now = datetime.now()
        days_until_next_sunday = (6 - now.weekday()) if now.weekday() != 6 else 0
        next_reset = now + timedelta(days=days_until_next_sunday)
        next_reset = next_reset.replace(hour=0, minute=0, second=0, microsecond=0)
        wait_time = (next_reset - now).total_seconds()

        print(f"next counters reset: {next_reset}")
        await asyncio.sleep(wait_time)

        global join_count
        join_count = 0

        print("Weekly counter reset " + datetime.now())
        await asyncio.sleep(7*24*60*60)


client.run(BOT_TOKEN)