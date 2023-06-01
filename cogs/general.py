""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""

import os
import platform
import random

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks


class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="help", description="List all commands the bot has loaded"
    )
    @checks.not_blacklisted()
    async def help(self, context: Context) -> None:
        admin = list(os.environ.get("owners").split(","))
        embed = discord.Embed(
            title="Help :man_mechanic:", 
            description=f"Ask <@{int(admin[0])}> for help.\n[Klik hier voor meer info om berichten toe te voegen/te verwijderen](https://github.com/SDeVuyst/WhereContextbot3)\nList of available commands:", 
            color=0xF4900D
        )
        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()

            data = []
            for command in commands:
                description = command.description.partition("\n")[0]
                data.append(f"{command.name} - {description}")

            if i == "context":
                data.append("Rechtermuisklik -> Apps -> Add Context - Add message")
                data.append("Rechtermuisklik -> Apps -> Remove Context - Remove message")

            help_text = "\n".join(data)
            if len(help_text) > 0:
                embed.add_field(
                    name=i.capitalize(), value=f"```{help_text}```", inline=False
                )
        
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="lien",
        description="LIEN LOCKDOWN",
    )
    @checks.is_owner()
    async def lien(self, context: Context) -> None:
        # kick grom
        try:
            grom = await context.guild.fetch_member(464400950702899211)
            await grom.kick(reason=":warning: ***LIEN LOCKDOWN*** :warning:")
        # grom kick error
        except:
            pass
        # stuur lockdown bericht
        embed = discord.Embed(
            title=":warning: ***LIEN LOCKDOWN*** :warning:",
            description="<@464400950702899211> has been kicked.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
        

    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive",
    )
    @checks.not_blacklisted()
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x39AC39 if (self.bot.latency * 1000) < 150 else 0xF4900D
        )
        await context.send(embed=embed)


    @commands.hybrid_command(
        name="say",
        description="The bot will say anything you want",
    )
    @app_commands.describe(message="The message that should be repeated by the bot")
    @checks.not_blacklisted()
    async def say(self, context: Context, *, message: str) -> None:
        """
        The bot will say anything you want.

        :param context: The hybrid command context.
        :param message: The message that should be repeated by the bot.
        """
        await context.send(message)


    @commands.hybrid_command(
        name="embed",
        description="The bot will say anything you want, but within embeds",
    )
    @app_commands.describe(message="The message that should be repeated by the bot")
    @checks.not_blacklisted()
    async def embed(self, context: Context, *, message: str) -> None:
        """
        The bot will say anything you want, but using embeds.

        :param context: The hybrid command context.
        :param message: The message that should be repeated by the bot.
        """
        embed = discord.Embed(title=message, color=0xF4900D)
        await context.send(embed=embed)



async def setup(bot):
    await bot.add_cog(General(bot))
