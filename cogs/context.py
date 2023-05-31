from discord.ext import commands
from discord.ext.commands import Context
import discord
from discord import app_commands
from helpers import checks, db_manager


# Here we name the cog and create a new class for the cog.
class Context(commands.Cog, name="context"):
    def __init__(self, bot):
        self.bot = bot
        self.ctx_menu_add = app_commands.ContextMenu(
            name='Add Context',
            callback=self.context_add,
        )
        self.bot.tree.add_command(self.ctx_menu_add)

        self.ctx_menu_remove = app_commands.ContextMenu(
            name='Remove Context',
            callback=self.context_remove,
        )
        self.bot.tree.add_command(self.ctx_menu_remove)

    @checks.not_blacklisted()
    async def context_add(self, interaction: discord.Interaction, message:discord.Message):
        """
        Lets you add a message to the OOC game.

        """
        submitted_id = interaction.user.id

        if await db_manager.is_in_ooc(message.id):
            embed = discord.Embed(
                description=f"**{message.id}** is already in the game.",
                color=0xE02B2B,
            )
            await interaction.response.send_message(embed=embed)
            return
        
        total = await db_manager.add_message_to_ooc(message.id, submitted_id)

        # error
        if total == -1:
            embed = discord.Embed(
                description=f"Er is iets misgegaan.",
                color=0xE02B2B,
            )
            await interaction.response.send_message(embed=embed)
            return
        
        # alles oke
        embed = discord.Embed(
            description=f"**{message.id}** has been successfully added to the game",
            color=0x39AC39,
        )
        embed.set_footer(
            text=f"There {'is' if total == 1 else 'are'} now {total} {'message' if total == 1 else 'messages'} in the game"
        )
        await interaction.response.send_message(embed=embed)



    @checks.not_blacklisted()
    async def context_remove(self, interaction: discord.Interaction, message:discord.Message):
        """
        Lets you remove a message to the OOC game.

        """
        submitted_id = interaction.user.id

        if not await db_manager.is_in_ooc(message.id):
            embed = discord.Embed(
                description=f"**{message.id}** is not in the game.",
                color=0xE02B2B,
            )
            await interaction.response.send_message(embed=embed)
            return
        
        total = await db_manager.remove_message_from_ooc(message.id)

        # error
        if total == -1:
            embed = discord.Embed(
                description=f"Er is iets misgegaan.",
                color=0xE02B2B,
            )
            await interaction.response.send_message(embed=embed)
            return
        
        # alles oke
        embed = discord.Embed(
            description=f"**{message.id}** has been successfully removed from the game",
            color=0x39AC39,
        )
        embed.set_footer(
            text=f"There {'is' if total == 1 else 'are'} now {total} {'message' if total == 1 else 'messages'} in the game"
        )
        await interaction.response.send_message(embed=embed)


    @commands.hybrid_command(
        name="play",
        description="Play the out of context game",
    )
    @checks.not_blacklisted()
    async def play(self, context: Context) -> None:
        """
        Play the out of context game

        :param context: The hybrid command context.
        """
        messages = await db_manager.get_ooc_messages(10)
        
        # Geen berichten
        if len(messages) == 0:
            embed = discord.Embed(
                description="There are no messages.", color=0xF4900D
            )
            await context.send(embed=embed)
            return
        
        # error
        elif messages[0] == -1:
            embed = discord.Embed(
                title=f"Something went wrong",
                description=messages[1],
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return

        # alles is ok
        embed = discord.Embed(title="Out of Context", color=0xF4900D)
        messages_formatted = []
        for m in messages:    
            print(type(m))
            messages_formatted.append(f"• [{m}]({m.jump_url})")

        embed.description = "\n".join(messages)
        await context.send(embed=embed)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Context(bot))