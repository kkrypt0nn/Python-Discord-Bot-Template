
from discord.ext import commands
import os
from discord import app_commands
from discord.ext.commands import Context
import discord
import asyncio
from helpers import checks


# Here we name the cog and create a new class for the cog.
class Audio(commands.Cog, name="audio"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="join", description="bot joins voice channel")
    @checks.not_blacklisted()
    async def join(self, context: Context):
        try:
            if not context.message.author.voice:
                embed = discord.Embed(
                    title=f"You are not in a voice channel",
                    color=0xE02B2B
            ) 
            else:
                channel = context.author.voice.channel
                await channel.connect()
                embed = discord.Embed(
                    title=f"Joined channel {channel.name}!",
                    color=0x39AC39
                )
        except discord.ClientException:
            embed = discord.Embed(
                title=f"Already in voice channel",
                color=0xE02B2B
            )
            
        await context.send(embed=embed)

    
        

    @commands.hybrid_command(name="leave", description="bot leaves voice channel")
    @checks.not_blacklisted()
    async def leave(self, context: Context):

        voice_client = context.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
            embed = discord.Embed(
                title=f"left channel!",
                color=0x39AC39
            )
            await context.send(embed=embed)

        else:
            embed = discord.Embed(
                title=f"You are not in a voice channel",
                color=0xE02B2B
            )
            await context.send(embed=embed)
        
        

    @commands.hybrid_command(name="soundboard", description="Play snippet from soundboard")
    @checks.not_blacklisted()
    async def soundboard(self, context: Context):
    
        # try :
        server = context.message.guild
        vc = server.voice_client

        vc.play(discord.FFmpegPCMAudio(f"{os.path.realpath(os.path.dirname(__file__))}/../audio_snippets/sample-3s.mp3"), after=lambda e: print(f'finished playing'))

        # except:
        #     await context.send("The bot is not connected to a voice channel.")



# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Audio(bot))
