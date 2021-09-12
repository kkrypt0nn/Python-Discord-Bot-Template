""""
Copyright © Krypton 2021 - https://github.com/kkrypt0nn
Description:
This is a template to create your own discord bot in python.

Version: 3.0
"""

import json
import os
import sys

import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from helpers import json_manager

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class owner(commands.Cog, name="owner"):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="shutdown",
        description="Make the bot shutdown.",
    )
    async def shutdown(self, context: SlashContext):
        """
        Make the bot shutdown.
        """

        # This is, for now, only temporary
        with open("blacklist.json") as file:
            blacklist = json.load(file)
        if context.author.id in blacklist["ids"]:
            return

        if context.author.id in config["owners"]:
            embed = discord.Embed(
                description="Shutting down. Bye! :wave:",
                color=0x42F56C
            )
            await context.send(embed=embed)
            await self.bot.close()
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @cog_ext.cog_slash(
        name="say",
        description="The bot will say anything you want.",
        options=[
            create_option(
                name="message",
                description="The message you want me to repeat.",
                option_type=3,
                required=True
            )
        ],
    )
    async def say(self, context, message: str):
        """
        The bot will say anything you want.
        """

        # This is, for now, only temporary
        with open("blacklist.json") as file:
            blacklist = json.load(file)
        if context.author.id in blacklist["ids"]:
            return

        if context.author.id in config["owners"]:
            await context.send(message)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @cog_ext.cog_slash(
        name="embed",
        description="The bot will say anything you want, but within embeds.",
        options=[
            create_option(
                name="message",
                description="The message you want me to repeat.",
                option_type=3,
                required=True
            )
        ],
    )
    async def embed(self, context, message: str):
        """
        The bot will say anything you want, but within embeds.
        """

        # This is, for now, only temporary
        with open("blacklist.json") as file:
            blacklist = json.load(file)
        if context.author.id in blacklist["ids"]:
            return

        if context.author.id in config["owners"]:
            embed = discord.Embed(
                description=message,
                color=0x42F56C
            )
            await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @cog_ext.cog_slash(
        name="blacklist",
        description="Get the list of all blacklisted users.",
    )
    async def blacklist(self, context: SlashContext):
        """
        Lets you add or remove a user from not being able to use the bot.
        """

        # This is, for now, only temporary
        with open("blacklist.json") as file:
            blacklist = json.load(file)
        if context.author.id in blacklist["ids"]:
            return

        if context.invoked_subcommand is None:
            with open("blacklist.json") as file:
                blacklist = json.load(file)
            embed = discord.Embed(
                title=f"There are currently {len(blacklist['ids'])} blacklisted IDs",
                description=f"{', '.join(str(id) for id in blacklist['ids'])}",
                color=0x0000FF
            )
            await context.send(embed=embed)

    @cog_ext.cog_subcommand(
        base="blacklist",
        name="add",
        description="Lets you add a user from not being able to use the bot.",
        options=[
            create_option(
                name="user",
                description="The user you want to add to the blacklist.",
                option_type=6,
                required=True
            )
        ],
    )
    async def blacklist_add(self, context: SlashContext, user: discord.User = None):
        """
        Lets you add a user from not being able to use the bot.
        """

        # This is, for now, only temporary
        with open("blacklist.json") as file:
            blacklist = json.load(file)
        if context.author.id in blacklist["ids"]:
            return

        if context.author.id in config["owners"]:
            userID = user.id
            try:
                with open("blacklist.json") as file:
                    blacklist = json.load(file)
                if (userID in blacklist['ids']):
                    embed = discord.Embed(
                        title="Error!",
                        description=f"**{user.name}** is already in the blacklist.",
                        color=0xE02B2B
                    )
                    await context.send(embed=embed)
                    return
                json_manager.add_user_to_blacklist(userID)
                embed = discord.Embed(
                    title="User Blacklisted",
                    description=f"**{user.name}** has been successfully added to the blacklist",
                    color=0x42F56C
                )
                with open("blacklist.json") as file:
                    blacklist = json.load(file)
                embed.set_footer(
                    text=f"There are now {len(blacklist['ids'])} users in the blacklist"
                )
                await context.send(embed=embed)
            except:
                embed = discord.Embed(
                    title="Error!",
                    description=f"An unknown error occurred when trying to add **{user.name}** to the blacklist.",
                    color=0xE02B2B
                )
                await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @cog_ext.cog_subcommand(
        base="blacklist",
        name="remove",
        description="Lets you remove a user from not being able to use the bot.",
        options=[
            create_option(
                name="user",
                description="The user you want to remove from the blacklist.",
                option_type=6,
                required=True
            )
        ],
    )
    async def blacklist_remove(self, context, user: discord.User = None):
        """
        Lets you remove a user from not being able to use the bot.
        """

        # This is, for now, only temporary
        with open("blacklist.json") as file:
            blacklist = json.load(file)
        if context.author.id in blacklist["ids"]:
            return

        if context.author.id in config["owners"]:
            userID = user.id
            try:
                json_manager.remove_user_from_blacklist(userID)
                embed = discord.Embed(
                    title="User removed from blacklist",
                    description=f"**{user.name}** has been successfully removed from the blacklist",
                    color=0x42F56C
                )
                with open("blacklist.json") as file:
                    blacklist = json.load(file)
                embed.set_footer(
                    text=f"There are now {len(blacklist['ids'])} users in the blacklist"
                )
                await context.send(embed=embed)
            except:
                embed = discord.Embed(
                    title="Error!",
                    description=f"**{user.name}** is not in the blacklist.",
                    color=0xE02B2B
                )
                await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0xE02B2B
            )
            await context.send(embed=embed)


def setup(bot):
    bot.add_cog(owner(bot))
