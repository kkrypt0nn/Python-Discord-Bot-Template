from discord.ext import commands
from discord.ext.commands import Context
import discord
from helpers import checks


# Here we name the cog and create a new class for the cog.
class Context(commands.Cog, name="Out of Context"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="addContext",
        description="Voeg een bericht toe aan het out of context spel.",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def addContext(self, context: Context, message_ID: str, about: str):
        """
        Add a message to the out of context game

        :param context: The application command context.
        """
        embed = discord.Embed(
            title="Not yet implemented",
            color=0xF4900D,
        )
        await context.send(embed=embed)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Context(bot))