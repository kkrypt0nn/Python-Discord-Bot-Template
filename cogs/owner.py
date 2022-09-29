""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 5.1
"""

import json
import os
import sys

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks
from helpers import db_manager

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

class Owner(commands.Cog, name="owner"):
    def __init__(self, bot):
        self.bot = bot
    
    DEV_GUILD = discord.Object(id=config["dev_guild_id"])

    @commands.hybrid_command(
        name="sync",
        description="Synchonizes the slash commands.",
    )
    @checks.is_owner()
    @app_commands.guilds(DEV_GUILD)
    async def sync(self, context: Context) -> None:
        """
        Synchonizes the slash commands.

        :param context: The hybrid command context.
        """
        await self.bot.tree.sync()
        embed = discord.Embed(
            title="Slash Commands Sync",
            description="Slash commands have been synchronized.",
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="unsync",
        description="Unsynchonizes the slash commands.",
    )
    @checks.is_owner()
    @app_commands.guilds(DEV_GUILD)
    async def unsync(self, context: Context) -> None:
        """
        Unsynchonizes the slash commands.

        :param context: The hybrid command context.
        """
        self.bot.tree.clear_commands(guild=None)
        await self.bot.tree.sync()
        embed = discord.Embed(
            title="Slash Commands Unsync",
            description="Slash commands have been unsynchronized.",
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="load",
        description="Load a cog",
    )
    @app_commands.describe(cog="The name of the cog to load")
    @checks.is_owner()
    async def load(self, context: Context, cog: str) -> None:
        """
        The bot will load the given cog.

        :param context: The hybrid command context.
        :param cog: The name of the cog to load.
        """
        try:
            await self.bot.load_extension(f"cogs.{cog}")
        except Exception as e:
            embed = discord.Embed(
                title="Error!",
                description=f"Could not load the `{cog}` cog."
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            title="Load",
            description=f"Successfully loaded the `{cog}` cog."
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="unload",
        description="Unloads a cog.",
    )
    @app_commands.describe(cog="The name of the cog to unload")
    @checks.is_owner()
    async def unload(self, context: Context, cog: str) -> None:
        """
        The bot will unload the given cog.

        :param context: The hybrid command context.
        :param cog: The name of the cog to unload.
        """
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
        except Exception as e:
            embed = discord.Embed(
                title="Error!",
                description=f"Could not unload the `{cog}` cog."
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            title="Unload",
            description=f"Successfully loaded the `{cog}` cog."
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="reload",
        description="Reloads a cog.",
    )
    @app_commands.describe(cog="The name of the cog to reload")
    @checks.is_owner()
    async def reload(self, context: Context, cog: str) -> None:
        """
        The bot will reload the given cog.

        :param context: The hybrid command context.
        :param cog: The name of the cog to reload.
        """
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
        except Exception as e:
            embed = discord.Embed(
                title="Error!",
                description=f"Could not reload the `{cog}` cog."
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            title="Reload",
            description=f"Successfully reloaded the `{cog}` cog."
        )
        await context.send(embed=embed)    

    @commands.hybrid_command(
        name="shutdown",
        description="Make the bot shutdown.",
    )
    @checks.is_owner()
    async def shutdown(self, context: Context) -> None:
        """
        Shuts down the bot.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description="Shutting down. Bye! :wave:",
            color=0x9C84EF
        )
        await context.send(embed=embed)
        await self.bot.close()

    @commands.hybrid_command(
        name="say",
        description="The bot will say anything you want.",
    )
    @app_commands.describe(message="The message that should be repeated by the bot")
    @checks.is_owner()
    async def say(self, context: Context, message: str) -> None:
        """
        The bot will say anything you want.

        :param context: The hybrid command context.
        :param message: The message that should be repeated by the bot.
        """
        await context.send(message)

    @commands.hybrid_command(
        name="embed",
        description="The bot will say anything you want, but within embeds.",
    )
    @app_commands.describe(message="The message that should be repeated by the bot")
    @checks.is_owner()
    async def embed(self, context: Context, message: str) -> None:
        """
        The bot will say anything you want, but using embeds.

        :param context: The hybrid command context.
        :param message: The message that should be repeated by the bot.
        """
        embed = discord.Embed(
            description=message,
            color=0x9C84EF
        )
        await context.send(embed=embed)

    @commands.hybrid_group(
        name="blacklist",
        description="Get the list of all blacklisted users.",
    )
    @checks.is_owner()
    async def blacklist(self, context: Context) -> None:
        """
        Lets you add or remove a user from not being able to use the bot.

        :param context: The hybrid command context.
        """
        pass

    @blacklist.command(
        base="blacklist",
        name="add",
        description="Lets you add a user from not being able to use the bot.",
    )
    @app_commands.describe(user="The user that should be added to the blacklist")
    @checks.is_owner()
    async def blacklist_add(self, context: Context, user: discord.User) -> None:
        """
        Lets you add a user from not being able to use the bot.

        :param context: The hybrid command context.
        :param user: The user that should be added to the blacklist.
        """
        user_id = user.id
        if db_manager.is_blacklisted(user_id):
            embed = discord.Embed(
                title="Error!",
                description=f"**{user.name}** is not in the blacklist.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        total = db_manager.add_user_to_blacklist(user_id)
        embed = discord.Embed(
            title="User Blacklisted",
            description=f"**{user.name}** has been successfully added to the blacklist",
            color=0x9C84EF
        )
        embed.set_footer(
            text=f"There are now {total} {'user' if total == 1 else 'users'} in the blacklist"
        )
        await context.send(embed=embed)

    @blacklist.command(
        base="blacklist",
        name="remove",
        description="Lets you remove a user from not being able to use the bot.",
    )
    @app_commands.describe(user="The user that should be removed from the blacklist.")
    @checks.is_owner()
    async def blacklist_remove(self, context: Context, user: discord.User) -> None:
        """
        Lets you remove a user from not being able to use the bot.

        :param context: The hybrid command context.
        :param user: The user that should be removed from the blacklist.
        """
        user_id = user.id
        if not db_manager.is_blacklisted(user_id):
            embed = discord.Embed(
                title="Error!",
                description=f"**{user.name}** is already in the blacklist.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        total = db_manager.remove_user_from_blacklist(user_id)
        embed = discord.Embed(
            title="User removed from blacklist",
            description=f"**{user.name}** has been successfully removed from the blacklist",
            color=0x9C84EF
        )
        embed.set_footer(
            text=f"There are now {total} {'user' if total == 1 else 'users'} in the blacklist"
        )
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Owner(bot))
