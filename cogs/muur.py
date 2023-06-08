
from discord.ext import commands
from discord.ext.commands import Context
import discord
from helpers import checks


class Muur(commands.Cog, name="muur"):
    def __init__(self, bot):
        self.bot = bot

    def getEmbed(self, title, description, footer):
        embed = discord.Embed(
            title=title,
            description=description,
            color=0xF4900D
        )
        embed.set_footer(text=footer)
        return embed


    @commands.hybrid_group(
        name="muur",
        description="De OG quotes muur",
    )
    @checks.is_owner()
    async def muur(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="You need to specify a subcommand.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)


    @muur.command(
        base="muur",
        name="1",
        description="Keleos golden rule",
    )
    @checks.is_owner()
    async def muur_1(self, context: Context) -> None:
        await context.send(embed=self.getEmbed(
            "Keleos golden rule", 
            "You only need 3 things in life, happiness and good weather", 
            "-Keleo (golden rule)"
        ))


    @muur.command(
        base="muur",
        name="2",
        description="laten doen",
    )
    @checks.is_owner()
    async def muur_2(self, context: Context) -> None:
        await context.send(embed=self.getEmbed(
            "Free gible", 
            "Jij laat je toch ook altijd doen hé", 
            "-jeroentje pompoentje"
        ))


    @muur.command(
        base="muur",
        name="3",
        description=":skull:",
    )
    @checks.is_owner()
    async def muur_3(self, context: Context) -> None:
        await context.send(embed=self.getEmbed(
            "#stop cyberpesten", 
            "ik ken mijn limieten", 
            "-Yours truly"
        ))


    @muur.command(
        base="muur",
        name="4",
        description="the danny special",
    )
    @checks.is_owner()
    async def muur_4(self, context: Context) -> None:
        await context.send(embed=self.getEmbed(
            "the danny special", 
            "ik vertrouw je voor geen haar!!", 
            "-danny vande fucking veire"
        ))


    @muur.command(
        base="muur",
        name="5",
        description="L bozo",
    )
    @checks.is_owner()
    async def muur_5(self, context: Context) -> None:
        await context.send(embed=self.getEmbed(
            "Quote 5", 
            "L bozo", 
            "-bozarius III"
        ))

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Muur(bot))
