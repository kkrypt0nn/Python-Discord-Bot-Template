
from discord.ext import commands
import os
from discord import app_commands
from discord.ext.commands import Context
import discord
from helpers import checks, db_manager


# Here we name the cog and create a new class for the cog.
class Audio(commands.Cog, name="audio"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="join", description="bot joins voice channel")
    @checks.not_blacklisted()
    async def join(self, ctx):
        if not ctx.message.author.voice:
            embed = discord.Embed(
                title=f"You are not in a voice channel",
                color=0xE02B2B
            )
            ctx.send(embed=embed)
            return 
        
        channel = ctx.author.voice.channel
        await channel.connect()
        embed = discord.Embed(
            title=f"Joined channel!",
            color=0x39AC39
        )
        ctx.send(embed=embed)

    @commands.hybrid_command(name="leave", description="bot leaves voice channel")
    @checks.not_blacklisted()
    async def leave(self, ctx):

        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
            embed = discord.Embed(
                title=f"Joined channel!",
                color=0x39AC39
            )
            ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title=f"You are not in a voice channel",
                color=0xE02B2B
            )
            ctx.send(embed=embed)
        
        


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Audio(bot))
