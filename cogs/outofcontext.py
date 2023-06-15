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

        self.currently_playing = False


    @checks.not_blacklisted()
    async def context_add(self, interaction: discord.Interaction, message:discord.Message):
        """
        Lets you add a message to the OOC game.

        """
        submitted_id = interaction.user.id

        # check als message uit OOC komt
        if message.channel.id != int(os.environ.get('channel')):
            embed = discord.Embed(
                description="Bericht moet in #out-of-context staan!",
                color=0xE02B2B,
            )
            embed.set_footer(text=f"{message.id}")
            await interaction.response.send_message(embed=embed, delete_after=10, ephemeral=True)
            return

        # check als bericht al in db staat
        if await db_manager.is_in_ooc(message.id):
            embed = discord.Embed(
                description=f"Message is already in the game.",
                color=0xE02B2B,
            )
            embed.set_footer(text=f"{message.id}")
            await interaction.response.send_message(embed=embed, delete_after=10, ephemeral=True)
            return
        
        # voeg toe
        total = await db_manager.add_message_to_ooc(message.id, submitted_id)

        # error
        if total == -1:
            embed = discord.Embed(
                description=f"Er is iets misgegaan.",
                color=0xE02B2B,
            )
            embed.set_footer(text=f"{message.id}")
            await interaction.response.send_message(embed=embed)
            return
        
        # alles oke
        embed = discord.Embed(
            description=f"[Message]({message.jump_url}) has been added to the game",
            color=0x39AC39,
        )
        embed.set_footer(
            text=f"There {'is' if total == 1 else 'are'} now {total} {'message' if total == 1 else 'messages'} in the game"
        )
        await interaction.response.send_message(embed=embed, delete_after=10, ephemeral=True)


    @checks.not_blacklisted()
    async def context_remove(self, interaction: discord.Interaction, message:discord.Message):
        """
        Lets you remove a message to the OOC game.

        """
        embed = await self.remove(message.id, interaction.guild)
        await interaction.response.send_message(embed=embed, delete_after=10, ephemeral=True)


    async def remove(self, id, guild):
        # check als bericht bestaat
        if not await db_manager.is_in_ooc(id):
            embed = discord.Embed(
                description=f"**{id}** is not in the game.",
                color=0xE02B2B,
            )
            return embed
        
        # verwijder bericht
        total = await db_manager.remove_message_from_ooc(id)
    
        # error
        if total == -1:
            embed = discord.Embed(
                description=f"Er is iets misgegaan.",
                color=0xE02B2B,
            )
            return embed
        
        m = await guild.get_channel(int(os.environ.get("channel"))).fetch_message(id)
        
        # alles oke
        embed = discord.Embed(
            description=f"[Message]({m.jump_url}) has been removed from the game",
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
    @app_commands.describe(groep="Toon het spel ook aan andere personen")
    @checks.not_blacklisted()
    async def play(self, context: Context, groep: bool) -> None:
        """
        Play the out of context game

        :param context: The hybrid command context.
        """
        if self.currently_playing:
            embed = discord.Embed(
                description=f"Er is al iemand het spel aan het spelen.",
                color=0xE02B2B,
            )
            await context.send(embed=embed, delete_after=10)
            return
        
        embed, sendView = await self.getRandomMessage(context.guild)
        await self.menu.reset()
        self.menu.author = context.author
        await context.send(embed=embed, view= self.menu if sendView else None, ephemeral=not groep)
        self.currently_playing = True


    async def getRandomMessage(self, guild):
        # krijg random bericht uit db
        messages = await db_manager.get_ooc_messages(1)
        if len(messages) > 0:
            worked = await db_manager.increment_times_played(messages[0][0])

        # Geen berichten
        if len(messages) == 0:
            embed = discord.Embed(
                description="There are no messages.", color=0xF4900D
            )
            
            return (embed, False)
        
        # error
        elif messages[0] == -1 or not worked:
            embed = discord.Embed(
                title=f"Something went wrong",
                description=messages[1],
                color=0xE02B2B
            )
            return (embed, False)

        # alles is ok
        embed = await self.getEmbed(int(messages[0][0]), guild, messages[0][1], int(messages[0][2]), int(messages[0][3]))
        return (embed, True)
    

    async def getMessage(self, guild, id):
        # krijg bekend bericht uit db
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
        # haal bericht op van discord
        m = await guild.get_channel(int(os.environ.get("channel"))).fetch_message(id)
        desc = f"[Go to message]({m.jump_url})" if len(m.content) == 0 else f"**{m.content}**\n[Go to message]({m.jump_url})"
        embed = discord.Embed(
            title="**Out of Context**", 
            color=0xF4900D,
            description=desc
        )

        if m.attachments:
            # als er meerdere attachments zijn, tonen we enkel de eerste
            embed.set_image(url=m.attachments[0].url)

            # check als er video in message zit
            for attch in m.attachments:
                try:
                    if 'video' in attch.content_type:
                        embed.description += "\n**Contains video!**"

                # attachement type is onbekend
                except TypeError:
                    embed.description += "\n**Contains unknown attachment!**"

        try:
            user = await guild.fetch_member(int(added_by))
            embed.set_thumbnail(
                url=str(user.avatar.url)
            )

            embed.set_author(
                name=user.name, 
                icon_url=str(user.avatar.url)
            )

            embed.add_field(
                name="Times played",
                value=f"```{times_played}```",
                inline=True
            )

            # embed.add_field(
            #     name="Added by",
            #     # value=f"<@{int(added_by)}>",
            #     value = f"```{user.name}```",
            #     inline=True
            # )

            embed.add_field(
                name="Added at",
                value=f"```{added_at.strftime('%d/%m/%Y - %H:%M:%S')}```",
                inline=True
            )

            embed.set_footer(
                text=f"message id: {id}"
            )

        except Exception as e:
            embed.add_field(
                name="User error",
                value=e,
                inline=False
            )
        
        
        


        # voeg id toe aan messages indien nodig
        if self.menu.currentIndex == len(self.menu.messages):
            self.menu.messages.append(m.id)

        return embed



# behandelt alle knoppen
class Menu(discord.ui.View):
    def __init__(self, OOC):
        super().__init__(timeout=None)
        self.OOC = OOC
        self.messages = []
        self.currentIndex = 0
        self.messagesPlayed = 0
        self.author = None

    async def reset(self):
        for b in self.children:
            b.disabled = False




    @discord.ui.button(label="Previous", style=discord.ButtonStyle.green, disabled=True)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentIndex -= 1
        self.currentIndex = self.currentIndex if self.currentIndex > 0 else 0

        # disable previous knop als we op eerste bericht zitten
        if self.currentIndex == 0:
            for b in self.children:
                b.disabled = b.label == "Previous"
                

        # Toon het vorige bericht
        embed, showView = await self.OOC.getMessage(interaction.guild, self.messages[self.currentIndex])
        await interaction.response.edit_message(embed=embed, view = self if showView else None)


    @discord.ui.button(label="Next", style=discord.ButtonStyle.green)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentIndex += 1
        # check als we bericht al hebben ingeladen of nieuw random bericht moeten opvragen
        if (self.currentIndex == len(self.messages)):
            embed, sendView = await self.OOC.getRandomMessage(interaction.guild)
            self.messagesPlayed += 1

        else:
            embed, sendView = await self.OOC.getMessage(interaction.guild, self.messages[self.currentIndex])

        # enable alle knoppen
        for c in self.children:
            c.disabled = False

        await interaction.response.edit_message(embed=embed, view = self if sendView else None)


    @discord.ui.button(label="Remove", style=discord.ButtonStyle.red)
    async def remove(self, interaction: discord.Interaction, button: discord.ui.Button):
        # verwijder bericht
        embed = await self.OOC.remove(self.messages[self.currentIndex], interaction.guild)

        # zet index juist en verwijder bericht ook uit ingeladen berichten
        messageToDelete = self.messages[self.currentIndex]
        self.messages = [i for i in self.messages if i != messageToDelete]
        self.currentIndex = len(self.messages)-1 # if len(self.messages) > 0 else -1

        # disable de verwijder knop
        for b in self.children:
            b.disabled = b.label == "Remove"
            # disable de previous knop als we op begin van lijst zitten
            if self.currentIndex == -1:
                b.disabled = b.label == "Previous" or b.label == "Remove"

        await interaction.response.edit_message(embed=embed, view=self)


    @discord.ui.button(label="Quit", style=discord.ButtonStyle.blurple)
    async def quit(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        # stuur confirmatie bericht
        embed = discord.Embed(
            title="Bye. :wave:",
            description=f"You played {self.messagesPlayed +1} {'message' if self.messagesPlayed == 0 else 'messages'}.",
            color=0xF4900D
        )
        await interaction.response.edit_message(embed=embed, view=None)

        # reset alle gegevens
        self.messages.clear()
        self.currentIndex = 0
        self.messagesPlayed = 0
        self.author = None

        await self.reset()

        self.OOC.currently_playing = False


    async def interaction_check(self, interaction: discord.Interaction):
        try:
            return interaction.user.id == self.author.id or str(interaction.user.id) in list(os.environ.get("owners").split(","))
        except:
            return False
        



# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(OutOfContext(bot))