
from discord.ext import commands
from discord.ext.commands import Context
import discord
from helpers import checks


class Muur(commands.Cog, name="muur"):
    def __init__(self, bot):
        self.bot = bot

    def getEmbed(self, title, footer):
        embed = discord.Embed(
            title=title,
            color=0xF4900D
        )
        embed.set_footer(text=footer)
        return embed


    @commands.hybrid_group(
        name="muur",
        description="De OG quotes muur",
    )
    @checks.not_blacklisted()
    async def muur(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="You need to specify a subcommand.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)


    @muur.command(
        base="muur",
        name="golden_rule",
        description="Keleos golden rule",
    )
    @checks.not_blacklisted()
    async def muur_1(self, context: Context) -> None:
        await context.send(embed=self.getEmbed(
            "You only need 3 things in life, happiness and good weather", 
            "-Keleo (golden rule)"
        ))


    @muur.command(
        base="muur",
        name="laten_doen",
        description="laten doen",
    )
    @checks.not_blacklisted()
    async def muur_2(self, context: Context) -> None:
        await context.send(embed=self.getEmbed(
            "Jij laat je toch ook altijd doen hé", 
            "-jeroentje pompoentje"
        ))


    @muur.command(
        base="muur",
        name="limieten",
        description=":skull:",
    )
    @checks.not_blacklisted()
    async def muur_3(self, context: Context) -> None:
        await context.send(embed=self.getEmbed(
            "ik ken mijn limieten", 
            "-Yours truly"
        ))


    @muur.command(
        base="muur",
        name="danny",
        description="the danny special",
    )
    @checks.not_blacklisted()
    async def muur_4(self, context: Context) -> None:
        await context.send(embed=self.getEmbed(
            "ik vertrouw je voor geen haar!!", 
            "-danny vande fucking veire"
        ))


    @muur.command(
        base="muur",
        name="bozo",
        description="L bozo",
    )
    @checks.not_blacklisted()
    async def muur_5(self, context: Context) -> None:
        await context.send(embed=self.getEmbed(
            "L bozo", 
            "-bozarius III"
        ))

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Muur(bot))
