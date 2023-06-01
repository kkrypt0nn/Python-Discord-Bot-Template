from discord.ext import commands
from discord.ext.commands import Context
import discord
import os
from discord import app_commands
from helpers import checks, db_manager


# Here we name the cog and create a new class for the cog.
class OutOfContext(commands.Cog, name="context"):
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

        self.menu = Menu(self)


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
        message = await self.getRandomMessage(context.guild)
        print(message)
        await context.send(embed=message[0], view= self.menu if message[1] else None)


    async def getRandomMessage(self, guild):
        messages = await db_manager.get_ooc_messages(10)

        # Geen berichten
        if len(messages) == 0:
            embed = discord.Embed(
                description="There are no messages.", color=0xF4900D
            )
            
            return (embed, False)
        
        # error
        elif messages[0] == -1:
            embed = discord.Embed(
                title=f"Something went wrong",
                description=messages[1],
                color=0xE02B2B
            )
            return (embed, False)

        # alles is ok
        embed = self.getEmbed(int(messages[0][0]), guild)
        return (embed, True)
        

    async def getEmbed(self, id, guild):
        embed = discord.Embed(title="Out of Context", color=0xF4900D)
        m = await guild.get_channel(
            int(os.environ.get("channel")).fetch_message(id)
        )

        embed.description = m.content

        # zet index juist
        if m in self.menu.messages:
            self.menu.currentIndex = self.menu.messages.index(m)
        else:
            self.menu.messages.append(m)
            self.menu.currentIndex = len(self.menu.currentIndex) -1

        
        return embed

class Menu(discord.ui.View):
    def __init__(self, OOC):
        super().__init__()
        self.value = None
        self.OOC = OOC
        self.messages = []
        self.currentIndex = -1
    

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.green, disabled=True)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentIndex -= 1
        embed = self.OOC.getEmbed(self.messages[self.currentIndex], interaction.guild)
        await interaction.response.edit_message(embed=embed, view = self)


    @discord.ui.button(label="Next", style=discord.ButtonStyle.green)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentIndex += 1

        if (self.currentIndex == len(self.messages) -1):
            embed, sendView = await self.OOC.getRandomMessage(interaction.guild)
        else:
            sendView = True
            embed = self.OOC.getEmbed(self.messages[self.currentIndex], interaction.guild)

        print(self.children)

        await interaction.response.edit_message(embed=embed, view = self if sendView else None)


    @discord.ui.button(label="Remove", style=discord.ButtonStyle.red)
    async def remove(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.OOC.context_remove(interaction, self.currentMessage)


    @discord.ui.button(label="Quit", style=discord.ButtonStyle.blurple)
    async def quit(self, interaction: discord.Interaction, button: discord.ui.Button):
        l = len(self.messages)
        f = 'message' if l == 1 else 'messages'
        
        embed = discord.Embed(
            title="Bye. :wave:",
            description=f"You played {l} {f}.",
            color=0xF4900D
        )
        await interaction.response.edit_message(embed=embed)
        self.value=False
        self.stop()



# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(OutOfContext(bot))