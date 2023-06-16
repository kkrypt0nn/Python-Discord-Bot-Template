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

from helpers import checks, db_manager


class Stats(commands.Cog, name="stats"):
    def __init__(self, bot):
        self.bot = bot



    @commands.hybrid_command(
        name="individuele_stats",
        description="Hoeveel keer een bepaalde persoon een command heeft uitgevoerd",
    )
    @app_commands.describe(user="Welke persoon")
    @app_commands.choices(command=[
        discord.app_commands.Choice(name="nCount", value="nCount"),
        discord.app_commands.Choice(name="play", value="play"),
        discord.app_commands.Choice(name="messages_played", value="messages_played"),
        discord.app_commands.Choice(name="messages_deleted", value="messages_deleted"),
    ])
    @checks.not_blacklisted()
    async def stats_individual(self, context: Context, user: discord.User, command: discord.app_commands.Choice[str]) -> None:
        count = await db_manager.get_command_count(user.id, command.value)
        # Geen berichten
        if len(count) == 0 or int(count[0][0]) == 0:
            embed = discord.Embed(
                description=f"**<@{user.id}> didn't use {command.value} yet.",
                color=0x39AC39
            )
            await context.send(embed=embed)
            return
        
        # error
        elif count[0] == -1:
            embed = discord.Embed(
                title=f"Something went wrong",
                description=count[1],
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return

        embed = discord.Embed(
            description=f"**<@{user.id}> used {command.value} ```{count[0][0]}``` times.",
            color=0xF4900D
        )

        await context.send(embed=embed)


    @commands.hybrid_command(name="changecommandcount", description="Change the command count of a user (admin only)")
    @app_commands.describe(user="Which users count")
    @app_commands.choices(command=[
        discord.app_commands.Choice(name="nCount", value="nCount"),
        discord.app_commands.Choice(name="play", value="play"),
        discord.app_commands.Choice(name="messages_played", value="messages_played"),
        discord.app_commands.Choice(name="messages_deleted", value="messages_deleted"),
    ])
    @checks.is_owner()
    async def changeNCount(self, context: Context, user: discord.User, command: discord.app_commands.Choice[str], amount: int):
        # krijg count uit db
        succes = await db_manager.set_command_count(command.value, user.id, amount)


        # verstuur embed
        desc = f"{command.value} count of <@{user.id}> is now {amount}" if succes else "Something went wrong"
        embed = discord.Embed(
            title="Succes!" if succes else "Oops!",
            description=desc,
            color=0x39AC39 if succes else 0xF4900D
        )
        await context.send(embed=embed)



async def setup(bot):
    await bot.add_cog(Stats(bot))
