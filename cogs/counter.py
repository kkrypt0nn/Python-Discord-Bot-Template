
from discord.ext import commands
import os
from discord import app_commands
from discord.ext.commands import Context
import discord
from helpers import checks


# Here we name the cog and create a new class for the cog.
class Counter(commands.Cog, name="counter"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ncount", description="AYO??")
    @checks.not_blacklisted()
    async def ncount(self, context: Context):
        embed = discord.Embed(
            description=f"TODO",
            color=0xF4900D
        )

        await context.send(embed=embed)
    



# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Counter(bot))
