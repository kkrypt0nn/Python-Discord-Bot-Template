
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

    @commands.hybrid_command(name="giblereact", description="OMG jonathan is so fine!!")
    @checks.not_blacklisted()
    async def giblereact(self, context: Context):
        file, embed = await self.get_embed("giblereact.jpg", context.message.author.id, "Sexy giby")
        await context.send(file=file, embed=embed)

    @commands.hybrid_command(name="wholesquadlaughing", description="damn bro you got the whole squad laughing")
    @checks.not_blacklisted()
    async def wholesquadlaughing(self, context: Context):
        file, embed = await self.get_embed("wholesquadlaughing.jpg", context.message.author.id, "Squad is laughing")
        await context.send(file=file, embed=embed)

    @commands.hybrid_command(name="notfunny", description="bro that wasn't even funny")
    @checks.not_blacklisted()
    async def notfunny(self, context: Context):
        file, embed = await self.get_embed("notfunny.jpg", context.message.author.id, "Not funny")
        await context.send(file=file, embed=embed)
    
    @commands.hybrid_command(name="uthought", description="sike u thought")
    @checks.not_blacklisted()
    async def uthought(self, context: Context):
        file, embed = await self.get_embed("uthought.jpg", context.message.author.id, "U thought")
        await context.send(file=file, embed=embed)
    

    async def get_embed(self, name, userid, title):
        embed = discord.Embed(
            title=title, 
            description=f"Requested by <@{int(userid)}>", 
            color=0xF4900D
        )
        file = discord.File(f"{os.path.realpath(os.path.dirname(__file__))}/../reactions/{name}", filename="image.png")
        embed.set_image(url="attachment://image.png")
        return file, embed




# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Reacties(bot))
