
import random
from discord.ext import commands
from discord.ext.commands import Context
import discord
from helpers import checks


# Here we name the cog and create a new class for the cog.
class Names(commands.Cog, name="namen"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="gible",
        description="gibby aka. smikkel aka capybara_Lover123",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def gible(self, context: Context):
        messages = ["daar gaat je base gible", "wapz tnt over gible z'n base", "KAAANKEERRRBEK GIBLE", "gif"]
        rand = random.choice(messages)

        if rand == "gif":
            embed = discord.Embed(
                color=0xF4900D
            )
            embed.set_image(url="https://cdn.discordapp.com/attachments/1114464141508345906/1115720385070121000/ezgif.com-video-to-gif.gif")
        else:
            embed = discord.Embed(
                title=rand,
                color=0xF4900D,
            )
        await context.send(embed=embed)


    @commands.hybrid_command(
        name="nootje",
        description="nootje aka lil_kid_lover69 aka tough_guy_04",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def nootje(self, context: Context):
        messages = ["meest intelligente nootje opmerking:", "stop met je fk reels"]
        
        embed = discord.Embed(
            title=random.choice(messages),
            color=0xF4900D,
        )
        await context.send(embed=embed)


    @commands.hybrid_command(
        name="pingy",
        description="pingy aka pingy1 aka pongy aka Lol",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def pingy(self, context: Context):
        messages = ["Lol", "Njom", "dolfein"]
        
        embed = discord.Embed(
            title=random.choice(messages),
            color=0xF4900D,
        )
        await context.send(embed=embed)


    @commands.hybrid_command(
        name="ba",
        description="ba duy aka ba aka duy aka badwie",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def ba(self, context: Context):
        messages = ["ba", "zo schattig :smiling_face_with_3_hearts:"]
        
        embed = discord.Embed(
            title=random.choice(messages),
            color=0xF4900D,
        )
        await context.send(embed=embed)


    @commands.hybrid_command(
        name="meng",
        description="meng aka mongwong aka da GOAT"
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def meng(self, context: Context):
        messages = ["meng shut the fuck up"]
        
        embed = discord.Embed(
            title=random.choice(messages),
            color=0xF4900D,
        )
        await context.send(embed=embed)


    @commands.hybrid_command(
        name="broodman",
        description="jasman aka yachini aka yashja"
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def broodman(self, context: Context):
        messages = [f"retarded ass mening nr. {random.randint(194892084, 294892084)}"]
        
        embed = discord.Embed(
            title=random.choice(messages),
            color=0xF4900D,
        )
        await context.send(embed=embed)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Names(bot))
