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
        embed = await self.remove(message.id)
        await interaction.response.send_message(embed=embed)


    async def remove(self, id):
        if not await db_manager.is_in_ooc(id):
            embed = discord.Embed(
                description=f"**{id}** is not in the game.",
                color=0xE02B2B,
            )
            return embed
        
        total = await db_manager.remove_message_from_ooc(id)
    
        # error
        if total == -1:
            embed = discord.Embed(
                description=f"Er is iets misgegaan.",
                color=0xE02B2B,
            )
            return embed
        
        # alles oke
        embed = discord.Embed(
            description=f"**{id}** has been successfully removed from the game",
            color=0x39AC39,
        )
        embed.set_footer(
            text=f"There {'is' if total == 1 else 'are'} now {total} {'message' if total == 1 else 'messages'} in the game"
        )
        return embed


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
        embed, sendView = await self.getRandomMessage(context.guild)
        await context.send(embed=embed, view= self.menu if sendView else None)
        

    # TODO increment times_played
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
        embed = await self.getEmbed(int(messages[0][0]), guild, messages[0][1], int(messages[0][2]), int(messages[0][3]))
        return (embed, True)
    
    # TODO increment times_played
    async def getMessage(self, guild, id):
        messages = await db_manager.get_ooc_message(id)

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
        embed = await self.getEmbed(int(messages[0][0]), guild, messages[0][1], int(messages[0][2]), int(messages[0][3]))
        return (embed, True)
        

    async def getEmbed(self, id, guild, added_at, added_by, times_played):
        
        m = await guild.get_channel(int(os.environ.get("channel"))).fetch_message(id)
        embed = discord.Embed(
            title="Out of Context", 
            color=0xF4900D,
            description = f"```{m.content}```"
        )

        if m.attachments:
            print(m.attachments)

        embed.add_field(
            name="Extra info",
            value=f"Times played: {times_played}\nAdded by: <@{int(added_by)}>\nAdded at: {added_at}"
        )
        embed.set_footer(
            text=f"message id: {id}"
        )


        # voeg id toe aan messages indien nodig
        if self.menu.currentIndex == len(self.menu.messages):
            self.menu.messages.append(m.id)

        return embed

class Menu(discord.ui.View):
    def __init__(self, OOC):
        super().__init__()
        self.OOC = OOC
        self.messages = []
        self.currentIndex = 0
    

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.green, disabled=True)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentIndex -= 1
        if self.currentIndex == 0:
            # TODO disable de previous knop
            pass
        embed, showView = await self.OOC.getMessage(interaction.guild, self.messages[self.currentIndex])
        await interaction.response.edit_message(embed=embed, view = self if showView else None)


    @discord.ui.button(label="Next", style=discord.ButtonStyle.green)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentIndex += 1

        if (self.currentIndex == len(self.messages)):
            embed, sendView = await self.OOC.getRandomMessage(interaction.guild)
        else:
            embed, sendView = await self.OOC.getMessage(interaction.guild, self.messages[self.currentIndex])

        for c in self.children:
            c.disabled = False

        print(f"index is {self.currentIndex} and messages: {self.messages}")

        await interaction.response.edit_message(embed=embed, view = self if sendView else None)


    @discord.ui.button(label="Remove", style=discord.ButtonStyle.red)
    async def remove(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = await self.OOC.remove(self.messages[self.currentIndex])
        self.messages = [i for i in self.messages if i != self.messages[self.currentIndex]]
        self.currentIndex = len(self.messages) -1
        await interaction.response.send_message(embed=embed)


    @discord.ui.button(label="Quit", style=discord.ButtonStyle.blurple)
    async def quit(self, interaction: discord.Interaction, button: discord.ui.Button):
        l = len(self.messages)
        f = 'message' if l == 1 else 'messages'
        
        embed = discord.Embed(
            title="Bye. :wave:",
            description=f"You played {l} {f}.",
            color=0xF4900D
        )
        await interaction.response.edit_message(embed=embed, view=None)
        self.messages.clear()
        self.currentIndex = 0



# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(OutOfContext(bot))