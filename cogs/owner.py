""""
Copyright © Krypton 2021 - https://github.com/kkrypt0nn (https://krypt0n.co.uk)
Description:
This is a template to create your own discord bot in python.

Version: 4.0.1
"""

import json
import os
import sys

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands
from disnake.ext.commands import Context

from helpers import json_manager, checks

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class Owner(commands.Cog, name="owner"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="shutdown",
        description="Make the bot shutdown.",
    )
    @checks.is_owner()
    async def shutdown(self, interaction: ApplicationCommandInteraction):
        """
        Makes the bot shutdown.
        """
        embed = disnake.Embed(
            description="Shutting down. Bye! :wave:",
            color=0x9C84EF
        )
        await interaction.send(embed=embed)
        await self.bot.close()

    @commands.command(
        name="shutdown",
        description="Make the bot shutdown.",
    )
    @checks.is_owner()
    async def shutdown(self, context: Context):
        """
        Makes the bot shutdown.
        """
        embed = disnake.Embed(
            description="Shutting down. Bye! :wave:",
            color=0x9C84EF
        )
        await context.send(embed=embed)
        await self.bot.close()

    @commands.slash_command(
        name="say",
        description="The bot will say anything you want.",
        options=[
            Option(
                name="message",
                description="The message you want me to repeat.",
                type=OptionType.string,
                required=True
            )
        ],
    )
    @checks.is_owner()
    async def say(self, interaction: ApplicationCommandInteraction, message: str):
        """
        The bot will say anything you want.
        """
        await interaction.send(message)

    @commands.command(
        name="say",
        description="The bot will say anything you want.",
    )
    @checks.is_owner()
    async def say(self, context: Context, *, message: str):
        """
        The bot will say anything you want.
        """
        await context.send(message)

    @commands.slash_command(
        name="embed",
        description="The bot will say anything you want, but within embeds.",
        options=[
            Option(
                name="message",
                description="The message you want me to repeat.",
                type=OptionType.string,
                required=True
            )
        ],
    )
    @checks.is_owner()
    async def embed(self, interaction: ApplicationCommandInteraction, message: str):
        """
        The bot will say anything you want, but within embeds.
        """
        embed = disnake.Embed(
            description=message,
            color=0x9C84EF
        )
        await interaction.send(embed=embed)

    @commands.command(
        name="embed",
        description="The bot will say anything you want, but within embeds.",
    )
    @checks.is_owner()
    async def embed(self, context: Context, *, message: str):
        """
        The bot will say anything you want, but within embeds.
        """
        embed = disnake.Embed(
            description=message,
            color=0x9C84EF
        )
        await context.send(embed=embed)

    @commands.slash_command(
        name="blacklist",
        description="Get the list of all blacklisted users.",
    )
    @checks.is_owner()
    async def blacklist(self, interaction: ApplicationCommandInteraction):
        """
        Lets you add or remove a user from not being able to use the bot.
        """
        pass

    @commands.group(
        name="blacklist"
    )
    async def blacklist_normal(self,
                               context: Context):  # Here we need to rename the function name because of sub commands.
        """
        Lets you add or remove a user from not being able to use the bot.
        """
        if context.invoked_subcommand is None:
            with open("blacklist.json") as file:
                blacklist = json.load(file)
            embed = disnake.Embed(
                title=f"There are currently {len(blacklist['ids'])} blacklisted IDs",
                description=f"{', '.join(str(id) for id in blacklist['ids'])}",
                color=0x9C84EF
            )
            await context.send(embed=embed)

    @blacklist.sub_command(
        base="blacklist",
        name="add",
        description="Lets you add a user from not being able to use the bot.",
        options=[
            Option(
                name="user",
                description="The user you want to add to the blacklist.",
                type=OptionType.user,
                required=True
            )
        ],
    )
    @checks.is_owner()
    async def blacklist_add(self, interaction: ApplicationCommandInteraction, user: disnake.User = None):
        """
        Lets you add a user from not being able to use the bot.
        """
        try:
            user_id = user.id
            with open("blacklist.json") as file:
                blacklist = json.load(file)
            if user_id in blacklist['ids']:
                embed = disnake.Embed(
                    title="Error!",
                    description=f"**{user.name}** is already in the blacklist.",
                    color=0xE02B2B
                )
                return await interaction.send(embed=embed)
            json_manager.add_user_to_blacklist(user_id)
            embed = disnake.Embed(
                title="User Blacklisted",
                description=f"**{user.name}** has been successfully added to the blacklist",
                color=0x9C84EF
            )
            with open("blacklist.json") as file:
                blacklist = json.load(file)
            embed.set_footer(
                text=f"There are now {len(blacklist['ids'])} users in the blacklist"
            )
            await interaction.send(embed=embed)
        except Exception as exception:
            embed = disnake.Embed(
                title="Error!",
                description=f"An unknown error occurred when trying to add **{user.name}** to the blacklist.",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)
            print(exception)

    @blacklist_normal.command(
        name="add"
    )
    async def blacklist_add(self, context: Context, member: disnake.Member = None):
        """
        Lets you add a user from not being able to use the bot.
        """
        try:
            user_id = member.id
            with open("blacklist.json") as file:
                blacklist = json.load(file)
            if user_id in blacklist['ids']:
                embed = disnake.Embed(
                    title="Error!",
                    description=f"**{member.name}** is already in the blacklist.",
                    color=0xE02B2B
                )
                return await context.send(embed=embed)
            json_manager.add_user_to_blacklist(user_id)
            embed = disnake.Embed(
                title="User Blacklisted",
                description=f"**{member.name}** has been successfully added to the blacklist",
                color=0x9C84EF
            )
            with open("blacklist.json") as file:
                blacklist = json.load(file)
            embed.set_footer(
                text=f"There are now {len(blacklist['ids'])} users in the blacklist"
            )
            await context.send(embed=embed)
        except:
            embed = disnake.Embed(
                title="Error!",
                description=f"An unknown error occurred when trying to add **{member.name}** to the blacklist.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @blacklist.sub_command(
        base="blacklist",
        name="remove",
        description="Lets you remove a user from not being able to use the bot.",
        options=[
            Option(
                name="user",
                description="The user you want to remove from the blacklist.",
                type=OptionType.user,
                required=True
            )
        ],
    )
    @checks.is_owner()
    async def blacklist_remove(self, interaction: ApplicationCommandInteraction, user: disnake.User = None):
        """
        Lets you remove a user from not being able to use the bot.
        """
        try:
            json_manager.remove_user_from_blacklist(user.id)
            embed = disnake.Embed(
                title="User removed from blacklist",
                description=f"**{user.name}** has been successfully removed from the blacklist",
                color=0x9C84EF
            )
            with open("blacklist.json") as file:
                blacklist = json.load(file)
            embed.set_footer(
                text=f"There are now {len(blacklist['ids'])} users in the blacklist"
            )
            await interaction.send(embed=embed)
        except ValueError:
            embed = disnake.Embed(
                title="Error!",
                description=f"**{user.name}** is not in the blacklist.",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)
        except Exception as exception:
            embed = disnake.Embed(
                title="Error!",
                description=f"An unknown error occurred when trying to add **{user.name}** to the blacklist.",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)
            print(exception)

    @blacklist_normal.command(
        name="remove"
    )
    async def blacklist_remove(self, context, member: disnake.Member = None):
        """
        Lets you remove a user from not being able to use the bot.
        """
        try:
            user_id = member.id
            json_manager.remove_user_from_blacklist(user_id)
            embed = disnake.Embed(
                title="User removed from blacklist",
                description=f"**{member.name}** has been successfully removed from the blacklist",
                color=0x9C84EF
            )
            with open("blacklist.json") as file:
                blacklist = json.load(file)
            embed.set_footer(
                text=f"There are now {len(blacklist['ids'])} users in the blacklist"
            )
            await context.send(embed=embed)
        except:
            embed = disnake.Embed(
                title="Error!",
                description=f"**{member.name}** is not in the blacklist.",
                color=0xE02B2B
            )
            await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Owner(bot))
