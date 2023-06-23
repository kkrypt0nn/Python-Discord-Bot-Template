
import subprocess
from discord.ext import commands
import os
from discord import app_commands
from discord.ext.commands import Context
import discord
import asyncio
import tempfile
from helpers import checks, db_manager, http, ytdl
from discord.utils import get
from discord import FFmpegPCMAudio
import youtube_dl


# Here we name the cog and create a new class for the cog.
class Audio(commands.Cog, name="audio"):
    def __init__(self, bot):
        self.bot = bot
        ytdl_format_options = {
            'format': 'bestaudio/best',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
        }

        ffmpeg_options = {
            'options': '-vn'
        }

        self.ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

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

        vc = context.message.guild.voice_client
        if vc.is_connected():
            await vc.disconnect()
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
                

    @commands.hybrid_command(name="soundboard", description="Play effect from soundboard")
    @app_commands.choices(effect=[
        discord.app_commands.Choice(name="hentai Xander", value="hentai.mp3"),
        discord.app_commands.Choice(name="alexa... shut the fuck up", value="alexa.mp3"),
        discord.app_commands.Choice(name="yeah boy", value="yeah-boy.mp3"),
        discord.app_commands.Choice(name="sinister laugh", value="sinister-laugh.mp3"),
        discord.app_commands.Choice(name="help me n-", value="help-me.mp3"),
        discord.app_commands.Choice(name="illuminati", value="illuminati.mp3"),
        discord.app_commands.Choice(name="gta v wasted", value="gta-wasted.mp3"),
        discord.app_commands.Choice(name="surprise motherfucker", value="surprise.mp3"),
        discord.app_commands.Choice(name="the rock boom sound", value="the-rock.mp3"),
        discord.app_commands.Choice(name="ba laughing", value="ba-lach.mp3"),
        discord.app_commands.Choice(name="creeper", value="creeper.mp3"),
    ])
    @checks.not_blacklisted()
    async def soundboard(self, context: Context, effect: discord.app_commands.Choice[str]):
        if not context.message.author.voice:
            embed = discord.Embed(
                title=f"You are not in a voice channel",
                color=0xE02B2B
            ) 
            await context.send(embed=embed)
            return
        try:
            vc = context.message.guild.voice_client
            if not vc.is_connected():
                await context.invoke(self.bot.get_command('join'))

            vc.play(discord.FFmpegPCMAudio(f"{os.path.realpath(os.path.dirname(__file__))}/../audio_snippets/{effect.value}"))
            embed = discord.Embed(
                title=f"played {effect.name}!",
                color=0x39AC39
            )
            await context.send(embed=embed, ephemeral=True)

            # stats
            await db_manager.increment_or_add_command_count(context.author.id, "soundboard", 1)

        except Exception as e:
            embed = discord.Embed(
                title=f"Something went wrong",
                description=e,
                color=0xE02B2B
            )
            await context.send(embed=embed, ephemeral=True)


    @commands.hybrid_command(name="tts", description="Text to Speech")
    @app_commands.choices(voice=[
        discord.app_commands.Choice(name="Alexa", value="alexa"),
        discord.app_commands.Choice(name="Peter Griffin", value="peter-griffin"),
        discord.app_commands.Choice(name="Glenn Quagmire", value="quagmire"),
        discord.app_commands.Choice(name="Walter White", value="walter-white"),
        discord.app_commands.Choice(name="Saul Goodman", value="saul-goodman"),
        discord.app_commands.Choice(name="Barack Obama", value="barack-obama"),
        discord.app_commands.Choice(name="DIO (jp)", value="dio-jp"),
        discord.app_commands.Choice(name="PewDiePie", value="pewdiepie"),
        discord.app_commands.Choice(name="Hitler", value="hitler-rant"),
    ])
    @checks.not_blacklisted()
    @commands.cooldown(rate=1, per=120)
    async def tts(self, context: Context, speech: str, voice: discord.app_commands.Choice[str]):
        
        if not context.message.author.voice:
            embed = discord.Embed(
                title=f"You are not in a voice channel",
                color=0xE02B2B
            ) 
            await context.send(embed=embed)
            context.command.reset_cooldown(context)
            return
        
        vc = context.message.guild.voice_client
        if vc is None:
            embed = discord.Embed(
                title=f"Bot is not in vc",
                description="use /join to add bot to vc",
                color=0xE02B2B
            ) 
            await context.send(embed=embed)
            context.command.reset_cooldown(context)
            return      
            

        await context.defer()

        try:
            audio_data = await http.query_uberduck(speech, voice.value)
            with tempfile.NamedTemporaryFile(
                suffix=".wav"
            ) as wav_f, tempfile.NamedTemporaryFile(suffix=".opus") as opus_f:
                wav_f.write(audio_data.getvalue())
                wav_f.flush()
                subprocess.check_call(["ffmpeg", "-y", "-i", wav_f.name, opus_f.name])

                source = discord.FFmpegOpusAudio(opus_f.name)
                vc.play(source, after=None)

                while vc.is_playing():
                    await asyncio.sleep(0.5)
            
            embed = discord.Embed(
                title=f"Said ```{speech}``` in a {voice.name} voice!",
                color=0x39AC39
            )
            await context.interaction.followup.send(embed=embed)

            # stats
            await db_manager.increment_or_add_command_count(context.author.id, "tts", 1)


        except Exception as e:
            embed = discord.Embed(
                title=f"Error",
                description=e,
                color=0xE02B2B
            )
            await context.interaction.followup.send(embed=embed)




    @commands.hybrid_command(name="music-yt", description="play a single youtube video")
    @checks.is_owner()
    async def music_yt(self, context: Context, url: str):

        vc = context.message.guild.voice_client
        if vc is None:
            embed = discord.Embed(
                title=f"Bot is not in vc",
                description="use /join to add bot to vc",
                color=0xE02B2B
            ) 
            await context.send(embed=embed)
            return  
        
        await context.defer()
        
        filename = await ytdl.YTDLSource.from_url(url, loop=self.bot.loop)
        vc.play(discord.FFmpegPCMAudio(source=filename))

        await context.interaction.followup.send('**Now playing:** {}'.format(filename))



# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Audio(bot))
