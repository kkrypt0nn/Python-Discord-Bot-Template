
from discord.ext import commands
import os
from discord import app_commands
from discord.ext.commands import Context
import discord
from helpers import checks, db_manager


# Here we name the cog and create a new class for the cog.
class Counter(commands.Cog, name="counter"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ncount", description="AYO??")
    @app_commands.describe(user="Which users' n-word count")
    @checks.not_blacklisted()
    async def nCount(self, context: Context, user: discord.User):
        # krijg count bericht uit db
        count = await db_manager.get_nword_count(user.id)

        # Geen berichten
        if len(count) == 0 or int(count[0][0]) == 0:
            embed = discord.Embed(
                description=f"**NWord Count of <@{user.id}>:** ```0```",
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
            description=f"**NWord Count of <@{user.id}>:** ```{count[0][0]}```",
            color=0xF4900D
        )

        # stats
        await db_manager.increment_or_add_command_count(context.author.id, "nCount", 1)

        await context.send(embed=embed)
    

    @commands.hybrid_command(name="changencount", description="Change the count of a user (admin only)")
    @app_commands.describe(user="Which users' n-word count")
    @app_commands.describe(amount="Amount to set the count to")
    @checks.is_owner()
    async def changeNCount(self, context: Context, user: discord.User, amount: int):
        # krijg count uit db
        succes = await db_manager.set_nword_count(user.id, amount)

        # verstuur embed
        desc = f"NWord Count of <@{user.id}> is now {amount}" if succes else "Something went wrong"
        embed = discord.Embed(
            title="Succes!" if succes else "Oops!",
            description=desc,
            color=0x39AC39 if succes else 0xF4900D
        )
        await context.send(embed=embed)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Counter(bot))
