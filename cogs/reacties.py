
from discord.ext import commands
import os
from discord import app_commands
from discord.ext.commands import Context
import discord
from helpers import checks


# Here we name the cog and create a new class for the cog.
class Reacties(commands.Cog, name="reacties"):
    def __init__(self, bot):
        self.bot = bot
        self.choices = []

    @commands.hybrid_command(name="giblereact")
    @checks.not_blacklisted()
    async def giblereact(self, context: Context):
        await context.send(embed=await self.get_embed("giblereact.jpg", context.message.author.id))

    @commands.hybrid_command(name="wholesquadlaughing")
    @checks.not_blacklisted()
    async def wholesquadlaughing(self, context: Context):
        await context.send(embed=await self.get_embed("wholesquadlaughing.jpg", context.message.author.id))

    @commands.hybrid_command(name="notfunny")
    @checks.not_blacklisted()
    async def notfunny(self, context: Context):
        await context.send(embed=await self.get_embed("notfunny.jpg", context.message.author.id))
    
    @commands.hybrid_command(name="uthought")
    @checks.not_blacklisted()
    async def uthought(self, context: Context):
        await context.send(embed=await self.get_embed("uthought.jpg", context.message.author.id))
    

    async def get_embed(self, name, userid):
        embed = discord.Embed(
            title=name.split(".")[0].capitalize(), 
            description=f"Requested by <@{int(userid)}>", 
            color=0xF4900D
        )
        embed.set_image(url=f"{os.path.realpath(os.path.dirname(__file__))}/../reactions/{name}")
        return embed




# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Reacties(bot))
