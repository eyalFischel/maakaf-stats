import aiohttp
import asyncio
import configparser

# config file
config = configparser.ConfigParser()
config.read('config.ini')

BOT_TOKEN = config['discord']['BOT_TOKEN']
GUILD_ID = config['discord']['GUILD_ID']
discord_url = 'https://discord.com/api'
headers = {
    'Authorization': f'Bot {BOT_TOKEN}'
}


async def get_guild_members(session):
    url = discord_url + f'/guilds/{GUILD_ID}/members?limit=1000'

    async with session.get(url, headers=headers) as response:
        if response.status != 200:
            print(f'Error fetching members: {response.status}')
            return []
        
        members = await response.json()
        return members


async def get_guild_channels(session):
    url = discord_url + f'/guilds/{GUILD_ID}/channels'

    async with session.get(url, headers=headers) as response:
        if response.status != 200:
            print(f'Error fetching members: {response.status}')
            return []
        
        channels = await response.json()
        return channels


async def get_channel_messages(session, channel_id):
    url = discord_url + f'/channels/{channel_id}/messages'

    async with session.get(url, headers=headers) as response:
        if response.status != 200:
            print(f'Error fetching members: {response.status}')
            return []
        
        messages = await response.json()
        return messages


# sort members by join date and filter bot members
def sort_members(members):
        members_sorted_date = []
        
        for member in members:
            user = member['user']
            username = user['username']

            if 'bot' not in user:
                members_sorted_date.append((member['joined_at'], username))
        
        members_sorted_date.sort()
        return members_sorted_date

def filter_channels(channels):
    project_categories = set([c['id'] for c in channels if is_category(c) and is_projects_category(c)])
    project_text_channels = [c for c in channels if is_text_channel(c) and c['parent_id'] in project_categories]
    return project_text_channels

def is_category(channel):
    return channel['type'] == 4

def is_projects_category(channel):
    return channel['name'].lower().startswith('projects-')

def is_text_channel(channel):
    return channel['type'] == 0


async def main():
    async with aiohttp.ClientSession() as session:
        members = await get_guild_members(session)
        members = sort_members(members)
        channels = await get_guild_channels(session)
        channels = filter_channels(channels)
        

# Run the script
asyncio.run(main())