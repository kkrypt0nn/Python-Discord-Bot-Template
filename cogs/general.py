""""
Copyright © Krypton 2021 - https://github.com/kkrypt0nn
Description:
This is a template to create your own discord bot in python.

Version: 3.0
"""

import json
import os
import platform
import random
import sys

import aiohttp
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class general(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    async def botinfo(self, context: SlashContext):
        """
        Get some useful (or not) information about the bot.
        """

        # This is, for now, only temporary
        with open("blacklist.json") as file:
            blacklist = json.load(file)
        if context.author.id in blacklist["ids"]:
            return

        embed = discord.Embed(
            description="Used Krypton's template",
            color=0x42F56C
        )
        embed.set_author(
            name="Bot Information"
        )
        embed.add_field(
            name="Owner:",
            value="Krypton#2188",
            inline=True
        )
        embed.add_field(
            name="Python Version:",
            value=f"{platform.python_version()}",
            inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"{config['bot_prefix']}",
            inline=False
        )
        embed.set_footer(
            text=f"Requested by {context.author}"
        )
        await context.send(embed=embed)

    @cog_ext.cog_slash(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    async def serverinfo(self, context: SlashContext):
        """
        Get some useful (or not) information about the server.
        """

        # This is, for now, only temporary
        with open("blacklist.json") as file:
            blacklist = json.load(file)
        if context.author.id in blacklist["ids"]:
            return

        server = context.guild
        roles = [x.name for x in server.roles]
        role_length = len(roles)
        if role_length > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)
        channels = len(server.channels)
        time = str(server.created_at)
        time = time.split(" ")
        time = time[0]

        embed = discord.Embed(
            title="**Server Name:**",
            description=f"{server}",
            color=0x42F56C
        )
        embed.set_thumbnail(
            url=server.icon_url
        )
        embed.add_field(
            name="Server ID",
            value=server.id
        )
        embed.add_field(
            name="Member Count",
            value=server.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{channels}"
        )
        embed.add_field(
            name=f"Roles ({role_length})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {time}"
        )
        await context.send(embed=embed)

    @cog_ext.cog_slash(
        name="ping",
        description="Check if the bot is alive.",
    )
    async def ping(self, context: SlashContext):
        """
        Check if the bot is alive.
        """

        # This is, for now, only temporary
        with open("blacklist.json") as file:
            blacklist = json.load(file)
        if context.author.id in blacklist["ids"]:
            return

        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x42F56C
        )
        await context.send(embed=embed)

    @cog_ext.cog_slash(
        name="invite",
        description="Get the invite link of the bot to be able to invite it.",
    )
    async def invite(self, context: SlashContext):
        """
        Get the invite link of the bot to be able to invite it.
        """

        # This is, for now, only temporary
        with open("blacklist.json") as file:
            blacklist = json.load(file)
        if context.author.id in blacklist["ids"]:
            return

        embed = discord.Embed(
            description=f"Invite me by clicking [here](https://discordapp.com/oauth2/authorize?&client_id={config['application_id']}&scope=bot&permissions=470150263).",
            color=0xD75BF4
        )
        try:
            # To know what permissions to give to your bot, please see here: https://discordapi.com/permissions.html and remember to not give Administrator permissions.
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)

    @cog_ext.cog_slash(
        name="server",
        description="Get the invite link of the discord server of the bot for some support.",
    )
    async def server(self, context: SlashContext):
        """
        Get the invite link of the discord server of the bot for some support.
        """

        # This is, for now, only temporary
        with open("blacklist.json") as file:
            blacklist = json.load(file)
        if context.author.id in blacklist["ids"]:
            return

        embed = discord.Embed(
            description=f"Join the support server for the bot by clicking [here](https://discord.gg/HzJ3Gfr).",
            color=0xD75BF4
        )
        try:
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)

    @cog_ext.cog_slash(
        name="poll",
        description="Create a poll where members can vote.",
        options=[
            create_option(
                name="title",
                description="The title of the poll.",
                option_type=3,
                required=True
            )
        ],
    )
    async def poll(self, context: SlashContext, title: str):
        """
        Create a poll where members can vote.
        """

        # This is, for now, only temporary
        with open("blacklist.json") as file:
            blacklist = json.load(file)
        if context.author.id in blacklist["ids"]:
            return

        embed = discord.Embed(
            title="A new poll has been created!",
            description=f"{title}",
            color=0x42F56C
        )
        embed.set_footer(
            text=f"Poll created by: {context.author} • React to vote!"
        )
        embed_message = await context.send(embed=embed)
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("👎")
        await embed_message.add_reaction("🤷")

    @cog_ext.cog_slash(
        name="8ball",
        description="Ask any question to the bot.",
        options=[
            create_option(
                name="question",
                description="The question you want to ask.",
                option_type=3,
                required=True
            )
        ],
    )
    async def eight_ball(self, context: SlashContext, question: str):
        """
        Ask any question to the bot.
        """

        # This is, for now, only temporary
        with open("blacklist.json") as file:
            blacklist = json.load(file)
        if context.author.id in blacklist["ids"]:
            return

        answers = ['It is certain.', 'It is decidedly so.', 'You may rely on it.', 'Without a doubt.',
                   'Yes - definitely.', 'As I see, yes.', 'Most likely.', 'Outlook good.', 'Yes.',
                   'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.',
                   'Cannot predict now.', 'Concentrate and ask again later.', 'Don\'t count on it.', 'My reply is no.',
                   'My sources say no.', 'Outlook not so good.', 'Very doubtful.']
        embed = discord.Embed(
            title="**My Answer:**",
            description=f"{answers[random.randint(0, len(answers))]}",
            color=0x42F56C
        )
        embed.set_footer(
            text=f"The question was: {question}"
        )
        await context.send(embed=embed)

    @cog_ext.cog_slash(
        name="bitcoin",
        description="Get the current price of bitcoin.",
    )
    async def bitcoin(self, context):
        """
        Get the current price of bitcoin.
        """

        # This is, for now, only temporary
        with open("blacklist.json") as file:
            blacklist = json.load(file)
        if context.author.id in blacklist["ids"]:
            return

        url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            embed = discord.Embed(
                title=":information_source: Info",
                description=f"Bitcoin price is: ${response['bpi']['USD']['rate']}",
                color=0x42F56C
            )
            await context.send(embed=embed)


def setup(bot):
    bot.add_cog(general(bot))
