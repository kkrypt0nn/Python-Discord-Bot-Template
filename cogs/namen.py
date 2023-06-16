
import random
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands
import discord
from helpers import checks, db_manager


# Here we name the cog and create a new class for the cog.
class Names(commands.Cog, name="namen"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="gible",
        description="gibby aka. smikkel aka capybara_Lover123",
    )
    @app_commands.choices(choices=[
        app_commands.Choice(name="random", value=-1),
        app_commands.Choice(name="rip_base", value=0),
        app_commands.Choice(name="tnt", value=1),
        app_commands.Choice(name="kkrbek", value=2),
        app_commands.Choice(name="dans", value=3),
    ])
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def gible(self, context: Context, choices: app_commands.Choice[int]):
        messages = ["daar gaat je base gible", "wapz tnt over gible z'n base", "KAAANKEERRRBEK GIBLE", "dans"]
        m = random.choice(messages) if choices.value == -1 else messages[choices.value]

        if m == "dans":
            embed = discord.Embed(
                color=0xF4900D
            )
            embed.set_image(url="https://cdn.discordapp.com/attachments/1114464141508345906/1115720385070121000/ezgif.com-video-to-gif.gif")
        else:
            embed = discord.Embed(
                title=m,
                color=0xF4900D,
            )
        await context.send(embed=embed)
        # stats
        await db_manager.increment_or_add_command_count(context.author.id, "gible", 1)


    @commands.hybrid_command(
        name="nootje",
        description="nootje aka lil_kid_lover69 aka tough_guy_04",
    )
    @app_commands.choices(choices=[
        app_commands.Choice(name="random", value=-1),
        app_commands.Choice(name="intelligent", value=0),
        app_commands.Choice(name="reels", value=1),
    ])
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def nootje(self, context: Context, choices: app_commands.Choice[int]):
        messages = ["meest intelligente nootje opmerking:", "stop met je fk reels"]
        m = random.choice(messages) if choices.value == -1 else messages[choices.value]

        embed = discord.Embed(
            title=m,
            color=0xF4900D,
        )
        await context.send(embed=embed)
        # stats
        await db_manager.increment_or_add_command_count(context.author.id, "nootje", 1)


    @commands.hybrid_command(
        name="pingy",
        description="pingy aka pingy1 aka pongy aka Lol",
    )
    @app_commands.choices(choices=[
        app_commands.Choice(name="random", value=-1),
        app_commands.Choice(name="Lol", value=0),
        app_commands.Choice(name="njom", value=1),
        app_commands.Choice(name="dolfein", value=2),
    ])
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def pingy(self, context: Context, choices: app_commands.Choice[int]):
        messages = ["Lol", "Njom", "dolfein"]
        m = random.choice(messages) if choices.value == -1 else messages[choices.value]

        embed = discord.Embed(
            title=m,
            color=0xF4900D,
        )
        await context.send(embed=embed)
        # stats
        await db_manager.increment_or_add_command_count(context.author.id, "pingy", 1)


    @commands.hybrid_command(
        name="ba",
        description="ba duy aka ba aka duy aka badwie",
    )
    @app_commands.choices(choices=[
        app_commands.Choice(name="random", value=-1),
        app_commands.Choice(name="ba", value=0),
        app_commands.Choice(name="schattig", value=1),
    ])
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def ba(self, context: Context, choices: app_commands.Choice[int]):
        messages = ["ba", "zo schattig :smiling_face_with_3_hearts:"]
        m = random.choice(messages) if choices.value == -1 else messages[choices.value]

        embed = discord.Embed(
            title=m,
            color=0xF4900D,
        )
        await context.send(embed=embed)
        # stats
        await db_manager.increment_or_add_command_count(context.author.id, "ba", 1)


    @commands.hybrid_command(
        name="meng",
        description="meng aka mongwong aka da GOAT"
    )
    @app_commands.choices(choices=[
        app_commands.Choice(name="random", value=-1),
        app_commands.Choice(name="shatap", value=0),
        app_commands.Choice(name="pun", value=1),
    ])
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def meng(self, context: Context, choices: app_commands.Choice[int]):
        messages = ["meng shut the fuck up", "nog 1 pun en ik SNAP"]
        m = random.choice(messages) if choices.value == -1 else messages[choices.value]
       
        embed = discord.Embed(
            title=m,
            color=0xF4900D,
        )
        await context.send(embed=embed)
        # stats
        await db_manager.increment_or_add_command_count(context.author.id, "meng", 1)


    @commands.hybrid_command(
        name="broodman",
        description="jasman aka yachini aka yashja"
    )
    @app_commands.choices(choices=[
        app_commands.Choice(name="random", value=-1),
        app_commands.Choice(name="mening", value=0),
    ])
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def broodman(self, context: Context, choices: app_commands.Choice[int]):
        messages = [f"retarded ass mening nr. {random.randint(194892084, 294892084)}"]
        m = random.choice(messages) if choices.value == -1 else messages[choices.value]
       
        embed = discord.Embed(
            title=m,
            color=0xF4900D,
        )
        await context.send(embed=embed)
        # stats
        await db_manager.increment_or_add_command_count(context.author.id, "broodman", 1)


    @commands.hybrid_command(
        name="keleo",
        description="the one and only",
    )
    @app_commands.choices(choices=[
        app_commands.Choice(name="random", value=-1),
        app_commands.Choice(name="rooftop_madness", value=0),
    ])
    @checks.not_blacklisted()
    async def keleo(self, context: Context, choices: app_commands.Choice[int]):
        messages = ["rooftop"]
        m = random.choice(messages) if choices.value == -1 else messages[choices.value]

        if m == "rooftop":
            embed = discord.Embed(
                color=0xF4900D
            )
            embed.set_image(url="https://cdn.discordapp.com/attachments/727476894106386504/1117027462015107164/keleo_gif.gif")
        else:
            embed = discord.Embed(
                title=m,
                color=0xF4900D,
            )
        await context.send(embed=embed)
        # stats
        await db_manager.increment_or_add_command_count(context.author.id, "keleo", 1)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Names(bot))
