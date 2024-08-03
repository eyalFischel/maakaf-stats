# import os
# import pytest
# from unittest.mock import AsyncMock, patch
# from discord.ext.test import message, start, stop
# from your_bot_module import DiscordBot, BOT_TOKEN, Session, insert_channel, insert_message, insert_user, update_channel

# @pytest.fixture(scope="function")
# def discord_bot():
#     intents = discord.Intents.default()
#     intents.members = True
#     bot = DiscordBot(intents=intents)
#     yield bot
#     stop()  # Stop the bot after each test

# @pytest.fixture
# def mock_session(mocker):
#     mock_session = mocker.patch("your_bot_module.Session", autospec=True)
#     return mock_session

# @pytest.mark.asyncio
# async def test_on_ready(discord_bot, mock_session, mocker):
#     mocker.patch.object(discord_bot, "guilds", new_callable=AsyncMock, return_value=[
#         AsyncMock(members=[AsyncMock(name="testuser", joined_at="2021-01-01")]),
#         AsyncMock(text_channels=[
#             AsyncMock(id=123, name="general", history=AsyncMock(return_value=[
#                 AsyncMock(id=1, author=AsyncMock(bot=False, name="testuser"), channel=AsyncMock(id=123), created_at="2021-01-01")
#             ]))
#         ])
#     ])
    
#     await discord_bot.on_ready()
    
#     mock_session.assert_called_once()

# @pytest.mark.asyncio
# async def test_on_message(discord_bot, mock_session):
#     message_mock = AsyncMock(author=AsyncMock(bot=False, name="testuser"), id=1, channel=AsyncMock(id=123, type=0), created_at="2021-01-01")
    
#     await discord_bot.on_message(message_mock)
    
#     mock_session.assert_called_once()

# @pytest.mark.asyncio
# async def test_on_guild_channel_create(discord_bot, mock_session):
#     channel_mock = AsyncMock(id=123, name="general")
    
#     await discord_bot.on_guild_channel_create(channel_mock)
    
#     mock_session.assert_called_once()

# @pytest.mark.asyncio
# async def test_on_member_join(discord_bot, mock_session):
#     member_mock = AsyncMock(name="testuser", joined_at="2021-01-01")
    
#     await discord_bot.on_member_join(member_mock)
    
#     mock_session.assert_called_once()

# @pytest.mark.asyncio
# async def test_on_guild_channel_update(discord_bot, mock_session):
#     before_mock = AsyncMock(name="oldname")
#     after_mock = AsyncMock(name="newname", id=123)
    
#     await discord_bot.on_guild_channel_update(before_mock, after_mock)
    
#     mock_session.assert_called_once()


# #generated example