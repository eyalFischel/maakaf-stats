import aiohttp
import asyncio
import configparser

# config file
config = configparser.ConfigParser()
config.read('config.ini')

# bot token and guild ID
BOT_TOKEN = config['discord']['BOT_TOKEN']
GUILD_ID = config['discord']['GUILD_ID']
discord_url = 'https://discord.com/api'
headers = {
    'Authorization': f'Bot {BOT_TOKEN}'
}

# get a list of the guild members and sort them by guild join date
async def get_guild_members(session):
    url = discord_url + f'/guilds/{GUILD_ID}/members?limit=1000'

    async with session.get(url, headers=headers) as response:
        if response.status != 200:
            print(f'Error fetching members: {response.status}')
            return []
        
        members = await response.json()
        members_sorted_date = []
        
        for member in members:
            user = member['user']
            username = user['username']

            if 'bot' not in user:
                members_sorted_date.append((member['joined_at'], username))
        
        members_sorted_date.sort()
        return members_sorted_date


# get a list of the guild channels
async def get_guild_channels(session):
    url = discord_url + f'/guilds/{GUILD_ID}/channels'

    async with session.get(url, headers=headers) as response:
        if response.status != 200:
            print(f'Error fetching members: {response.status}')
            return []
        
        channels = await response.json()
        project_categories = set([c['id'] for c in channels if c['type'] == 4 and c['name'].lower().startswith('projects-')])
        project_text_channels = [c for c in channels if c['type'] == 0 and c['parent_id'] in project_categories]
        return project_text_channels
            
async def main():
    async with aiohttp.ClientSession() as session:
        members = await get_guild_members(session)
        project_text_channels = await get_guild_channels(session)


# Run the script
asyncio.run(main())