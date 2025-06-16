import asyncio
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest
import discord
from discord.ext import commands


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def mock_bot():
    """Create a mock Discord bot instance."""
    bot = MagicMock(spec=commands.Bot)
    bot.user = MagicMock(spec=discord.User)
    bot.user.id = 123456789
    bot.user.name = "TestBot"
    bot.user.discriminator = "0000"
    bot.user.display_name = "TestBot"
    bot.user.mention = "<@123456789>"
    
    bot.guilds = []
    bot.loop = asyncio.get_event_loop()
    bot.wait_until_ready = AsyncMock()
    bot.load_extension = AsyncMock()
    bot.unload_extension = AsyncMock()
    bot.reload_extension = AsyncMock()
    
    return bot


@pytest.fixture
def mock_ctx():
    """Create a mock command context."""
    ctx = MagicMock(spec=commands.Context)
    
    # Mock author
    ctx.author = MagicMock(spec=discord.Member)
    ctx.author.id = 987654321
    ctx.author.name = "TestUser"
    ctx.author.display_name = "TestUser"
    ctx.author.discriminator = "1234"
    ctx.author.mention = "<@987654321>"
    ctx.author.bot = False
    
    # Mock guild
    ctx.guild = MagicMock(spec=discord.Guild)
    ctx.guild.id = 111222333
    ctx.guild.name = "Test Guild"
    ctx.guild.owner_id = 987654321
    
    # Mock channel
    ctx.channel = MagicMock(spec=discord.TextChannel)
    ctx.channel.id = 444555666
    ctx.channel.name = "test-channel"
    ctx.channel.send = AsyncMock()
    
    # Mock message
    ctx.message = MagicMock(spec=discord.Message)
    ctx.message.id = 777888999
    ctx.message.content = "!test command"
    ctx.message.delete = AsyncMock()
    
    # Mock send method
    ctx.send = AsyncMock()
    ctx.reply = AsyncMock()
    
    return ctx


@pytest.fixture
def mock_member():
    """Create a mock Discord member."""
    member = MagicMock(spec=discord.Member)
    member.id = 555666777
    member.name = "MockMember"
    member.display_name = "MockMember"
    member.discriminator = "5678"
    member.mention = "<@555666777>"
    member.bot = False
    member.roles = []
    member.top_role = MagicMock(spec=discord.Role)
    member.top_role.position = 1
    member.guild_permissions = discord.Permissions.all()
    
    return member


@pytest.fixture
def mock_role():
    """Create a mock Discord role."""
    role = MagicMock(spec=discord.Role)
    role.id = 888999000
    role.name = "Test Role"
    role.position = 5
    role.permissions = discord.Permissions.none()
    role.mention = "<@&888999000>"
    
    return role


@pytest.fixture
def mock_message():
    """Create a mock Discord message."""
    message = MagicMock(spec=discord.Message)
    message.id = 123123123
    message.content = "Test message content"
    message.created_at = discord.utils.utcnow()
    message.edited_at = None
    message.jump_url = "https://discord.com/channels/111222333/444555666/123123123"
    message.delete = AsyncMock()
    message.edit = AsyncMock()
    message.add_reaction = AsyncMock()
    
    return message


@pytest.fixture
def mock_embed():
    """Create a mock Discord embed."""
    embed = discord.Embed(
        title="Test Embed",
        description="This is a test embed",
        color=discord.Color.blue()
    )
    return embed


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_database(temp_dir):
    """Create a mock database connection."""
    import aiosqlite
    
    db_path = temp_dir / "test.db"
    
    async def get_db():
        db = await aiosqlite.connect(str(db_path))
        # Initialize with schema if needed
        with open("database/schema.sql", "r", encoding="utf-8") as f:
            await db.executescript(f.read())
        return db
    
    return get_db


@pytest.fixture
def mock_config():
    """Create a mock configuration."""
    return {
        "token": "test_token",
        "prefix": "!",
        "owner_ids": [987654321],
        "database_path": ":memory:",
        "log_level": "INFO",
    }


@pytest.fixture
def mock_cog(mock_bot):
    """Create a base mock cog."""
    cog = MagicMock(spec=commands.Cog)
    cog.bot = mock_bot
    return cog


@pytest.fixture(autouse=True)
def reset_discord_state():
    """Reset Discord.py's internal state between tests."""
    yield
    # Clean up any lingering state
    discord.client._loop = None