""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""

import json

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands

from helpers import json_manager, checks


class Owner(commands.Cog, name="owner-slash"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="shutdown",
        description="Make the bot shutdown.",
    )
    @checks.is_owner()
    async def shutdown(self, interaction: ApplicationCommandInteraction) -> None:
        """
        Makes the bot shutdown.
        :param interaction: The application command interaction.
        """
        embed = disnake.Embed(
            description="Shutting down. Bye! :wave:",
            color=0x9C84EF
        )
        await interaction.send(embed=embed)
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
    async def say(self, interaction: ApplicationCommandInteraction, message: str) -> None:
        """
        The bot will say anything you want.
        :param interaction: The application command interaction.
        :param message: The message that should be repeated by the bot.
        """
        await interaction.send(message)

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
    async def embed(self, interaction: ApplicationCommandInteraction, message: str) -> None:
        """
        The bot will say anything you want, but using embeds.
        :param interaction: The application command interaction.
        :param message: The message that should be repeated by the bot.
        """
        embed = disnake.Embed(
            description=message,
            color=0x9C84EF
        )
        await interaction.send(embed=embed)

    @commands.slash_command(
        name="blacklist",
        description="Get the list of all blacklisted users.",
    )
    @checks.is_owner()
    async def blacklist(self, interaction: ApplicationCommandInteraction) -> None:
        """
        Lets you add or remove a user from not being able to use the bot.
        :param interaction: The application command interaction.
        """
        pass

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
    async def blacklist_add(self, interaction: ApplicationCommandInteraction, user: disnake.User = None) -> None:
        """
        Lets you add a user from not being able to use the bot.
        :param interaction: The application command interaction.
        :param user: The user that should be added to the blacklist.
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
        :param interaction: The application command interaction.
        :param user: The user that should be removed from the blacklist.
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


def setup(bot):
    bot.add_cog(Owner(bot))
