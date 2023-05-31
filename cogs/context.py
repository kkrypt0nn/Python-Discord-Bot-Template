from discord.ext import commands
from discord.ext.commands import Context
import discord
from discord import app_commands
from helpers import checks, db_manager


# Here we name the cog and create a new class for the cog.
class Context(commands.Cog, name="context"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_group(
        name="context",
        description="Alles over out of context",
    )
    @checks.not_blacklisted()
    async def context(self, context: Context) -> None:
        """
        Lets you add or remove a user from not being able to use the bot.

        :param context: The hybrid command context.
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="You need to specify a subcommand.\n\n**Subcommands:**\n`add` - Add a user to the blacklist.\n`remove` - Remove a user from the blacklist.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)


    @context.command(
        base="context",
        name="add",
        description="Voeg een bericht toe aan het out of context spel",
    )
    @app_commands.describe(message_id="id van het bericht dat je wilt toevoegen")
    @app_commands.describe(about="Over wie gaat het bericht")
    @app_commands.describe(submitted_by="Wie heeft het bericht toegevoegd")

    @checks.not_blacklisted()
    async def context_add(self, context: Context, message_id: str, about: discord.User, submitted_by: discord.User) -> None:
        """
        Lets you add a message to the OOC game.

        :param context: The hybrid command context.
        :param message_id: The hybrid command context.
        :param about: The user about whom the message is.
        :param submitted_by: The user who submitted the message.
        """
        about_id = about.id
        submitted_id = submitted_by.id

        if await db_manager.is_in_ooc(message_id):
            embed = discord.Embed(
                description=f"**{message_id}** is already in the game.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return
        
        total = await db_manager.add_message_to_ooc(message_id, submitted_id, about_id)

        # error
        if total == -1:
            embed = discord.Embed(
                description=f"Er is iets misgegaan.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return
        
        # alles oke
        embed = discord.Embed(
            description=f"**{message_id}** has been successfully added to the game",
            color=0x39AC39,
        )
        embed.set_footer(
            text=f"There {'is' if total == 1 else 'are'} now {total} {'message' if total == 1 else 'messages'} in the game"
        )
        await context.send(embed=embed)




    @context.command(
        base="context",
        name="remove",
        description="Verwijder een bericht uit het out of context spel",
    )
    @app_commands.describe(message_id="id van het bericht dat je wilt verwijderen")
    @checks.not_blacklisted()
    async def context_remove(self, context: Context, message_id: str) -> None:
        """
        Lets you remove a message from the OOC game.

        :param context: The hybrid command context.
        :param message_id: id of the message to be deleted from db.
        """

        if not await db_manager.is_in_ooc(message_id):
            embed = discord.Embed(
                description=f"**{message_id}** is not in the game.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        
        total = await db_manager.remove_message_from_ooc(message_id)

        #error
        if total == -1:
            embed = discord.Embed(
                description=f"Er is iets misgegaan.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        
        # alles ok
        embed = discord.Embed(
            description=f"**{message_id}** has been successfully removed from the game",
            color=0x39AC39,
        )
        embed.set_footer(
            text=f"There {'is' if total == 1 else 'are'} now {total} {'message' if total == 1 else 'messages'} in the game"
        )
        await context.send(embed=embed)


    @context.command(
        base="context",
        name="play",
        description="Speel het out of context spel",
    )
    @checks.not_blacklisted()
    async def context_play(self, context: Context) -> None:
        """
        Play the out of context game

        :param context: The hybrid command context.
        """
        
        embed = discord.Embed(
            description=f"not yet implemented",
            color=0xE02B2B,
        )
        await context.send(embed=embed)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Context(bot))