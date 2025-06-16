"""Validation tests to ensure the testing infrastructure is set up correctly."""
import pytest
import discord
from discord.ext import commands


def test_pytest_is_working():
    """Test that pytest is installed and working."""
    assert True


def test_imports_working():
    """Test that all required imports are available."""
    import aiohttp
    import aiosqlite
    import pytest_mock
    import pytest_cov
    
    assert aiohttp is not None
    assert aiosqlite is not None
    assert pytest_mock is not None
    assert pytest_cov is not None


@pytest.mark.unit
def test_unit_marker():
    """Test that the unit marker is working."""
    assert True


@pytest.mark.integration
def test_integration_marker():
    """Test that the integration marker is working."""
    assert True


@pytest.mark.slow
def test_slow_marker():
    """Test that the slow marker is working."""
    import time
    time.sleep(0.1)
    assert True


def test_mock_bot_fixture(mock_bot):
    """Test that the mock_bot fixture works correctly."""
    assert isinstance(mock_bot, commands.Bot)
    assert mock_bot.user.id == 123456789
    assert mock_bot.user.name == "TestBot"


def test_mock_ctx_fixture(mock_ctx):
    """Test that the mock_ctx fixture works correctly."""
    assert isinstance(mock_ctx, commands.Context)
    assert mock_ctx.author.id == 987654321
    assert mock_ctx.guild.name == "Test Guild"
    assert mock_ctx.channel.name == "test-channel"


def test_mock_member_fixture(mock_member):
    """Test that the mock_member fixture works correctly."""
    assert isinstance(mock_member, discord.Member)
    assert mock_member.id == 555666777
    assert mock_member.name == "MockMember"


def test_mock_role_fixture(mock_role):
    """Test that the mock_role fixture works correctly."""
    assert isinstance(mock_role, discord.Role)
    assert mock_role.id == 888999000
    assert mock_role.name == "Test Role"


def test_mock_message_fixture(mock_message):
    """Test that the mock_message fixture works correctly."""
    assert isinstance(mock_message, discord.Message)
    assert mock_message.id == 123123123
    assert mock_message.content == "Test message content"


def test_mock_embed_fixture(mock_embed):
    """Test that the mock_embed fixture works correctly."""
    assert isinstance(mock_embed, discord.Embed)
    assert mock_embed.title == "Test Embed"
    assert mock_embed.description == "This is a test embed"


def test_temp_dir_fixture(temp_dir):
    """Test that the temp_dir fixture works correctly."""
    test_file = temp_dir / "test.txt"
    test_file.write_text("Hello, world!")
    
    assert test_file.exists()
    assert test_file.read_text() == "Hello, world!"


def test_mock_config_fixture(mock_config):
    """Test that the mock_config fixture works correctly."""
    assert mock_config["token"] == "test_token"
    assert mock_config["prefix"] == "!"
    assert 987654321 in mock_config["owner_ids"]


@pytest.mark.asyncio
async def test_async_functionality(mock_ctx):
    """Test that async tests work correctly."""
    await mock_ctx.send("Test message")
    mock_ctx.send.assert_called_once_with("Test message")


@pytest.mark.asyncio
async def test_mock_database_fixture(mock_database, temp_dir):
    """Test that the mock_database fixture works correctly."""
    # Skip if schema.sql doesn't exist
    import os
    if not os.path.exists("database/schema.sql"):
        pytest.skip("database/schema.sql not found")
    
    db_func = mock_database
    db = await db_func()
    
    # Test basic operations with warns table from schema
    await db.execute(
        "INSERT INTO warns (id, user_id, server_id, moderator_id, reason) VALUES (?, ?, ?, ?, ?)",
        (1, "123456789", "987654321", "555555555", "Test warning")
    )
    await db.commit()
    
    cursor = await db.execute("SELECT reason FROM warns WHERE id = ?", (1,))
    row = await cursor.fetchone()
    
    assert row is not None
    assert row[0] == "Test warning"
    
    await db.close()