import asyncio
from datetime import datetime, timedelta
import discord
from dotenv import load_dotenv
import os

intents = discord.Intents.default()
intents.members = True

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

client = discord.Client(intents=intents)

join_count = 0

# key: channel_name, value: [message_count, last_message_time] 
project_channels = {}
# key: member_name, value: {key: channel_name, val: [message_count, last_message_time]}
member_activity = {}

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

    asyncio.create_task(reset_counters_weekly())
    
    guild = client.get_guild(GUILD_ID)
    if not guild:
        print("guild not found")
    
    project_categories = [c for c in guild.categories if is_projects_category(c)]


@client.event
async def on_message(message):
    author = message.author
    channel = message.channel
    if message.author.bot:
        return
    
    if author.name not in member_activity:
        member_activity[author.name] = {}
    
    if channel.name not in member_activity[author.name]:
        member_activity[author.name][channel.name] = [0, 0]
    
    member_activity[author.name][channel.name][0] += 1
    member_activity[author.name][channel.name][1] = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
    print(member_activity)

    
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
        next_reset = now + timedelta(days=(6 - now.weekday()) % 7)
        next_reset = next_reset.replace(hour=0, minute=0, second=0, microsecond=0)
        wait_time = (next_reset - now).total_seconds()

        print(f"next counters reset: {next_reset}")
        await asyncio.sleep(wait_time)

        global join_count
        join_count = 0

        print("Weekly counter reset " + datetime.now())
        await asyncio.sleep(7*24*60*60)


def is_projects_category(category):
    return category.name.lower().startswith('projects-')

def is_text_channel(channel):
    return channel.type.value == 0


client.run(BOT_TOKEN)