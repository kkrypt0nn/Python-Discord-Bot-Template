import aiosqlite

# Utility 
# enabling and disabling of commands
# is_enable and is_disabled check for checking whether command is enabled or disabled

async def is_enabled(server_id: int, command_name: str) -> bool:
    """
    Check if a command is enabled.
    """
    async with aiosqlite.connect('database.db') as db:
        async with db.execute("SELECT disabled_commands FROM disabled_commands WHERE server_id = ?", (server_id,)) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return True  # If no commands are disabled, assume all are enabled
            disabled_commands = row[0].split(",")
            return True if command_name not in disabled_commands else False

async def is_disabled(server_id: int, command_name: str) -> bool:
    """
    Check if a command is disabled.
    """
    async with aiosqlite.connect('database.db') as db:
        async with db.execute("SELECT disabled_commands FROM disabled_commands WHERE server_id = ?", (server_id,)) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return False  # If no commands are disabled, assume all are enabled
            disabled_commands = row[0].split(",")
            return True if command_name in disabled_commands else False

async def get_disabled_commands(server_id: int) -> list:
    """
    Retrieve a list of disabled commands.
    """
    async with aiosqlite.connect('database.db') as db:
        async with db.execute("SELECT disabled_commands FROM disabled_commands WHERE server_id = ?", (server_id,)) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return []  # No commands are disabled
            return row[0].split(",") if row[0] else []

async def enable_command(server_id: int, command_name: str) -> None:
    """
    Enable a command for a specific server.
    """
    async with aiosqlite.connect('database.db') as db:
        async with db.execute("SELECT disabled_commands FROM disabled_commands WHERE server_id = ?", (server_id,)) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return  # No commands are disabled, nothing to enable
            disabled_commands = row[0].split(",")
            if command_name in disabled_commands:
                disabled_commands.remove(command_name)
                await db.execute("REPLACE INTO disabled_commands (server_id, disabled_commands) VALUES (?, ?)", (server_id, ",".join(disabled_commands)))
                await db.commit()
async def disable_command(server_id: int, command_name: str) -> None:
    """
    Disable a command for a specific server.
    """
    async with aiosqlite.connect('database.db') as db:
        async with db.execute("SELECT disabled_commands FROM disabled_commands WHERE server_id = ?", (server_id,)) as cursor:
            row = await cursor.fetchone()
            if row is None:
                disabled_commands = command_name
            else:
                disabled_commands = row[0]
                if command_name not in disabled_commands.split(","):
                    disabled_commands += f",{command_name}"
            await db.execute("REPLACE INTO disabled_commands (server_id, disabled_commands) VALUES (?, ?)", (server_id, disabled_commands))
            await db.commit()