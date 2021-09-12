""""
Copyright © Krypton 2021 - https://github.com/kkrypt0nn
Description:
This is a template to create your own discord bot in python.

Version: 3.0
"""

import json
import os
import sys

import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class moderation(commands.Cog, name="moderation"):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name='kick',
        description="Kick a user out of the server.",
        options=[
            create_option(
                name="user",
                description="The user you want to kick.",
                option_type=6,
                required=True
            ),
            create_option(
                name="reason",
                description="The reason you kicked the user.",
                option_type=3,
                required=False
            )
        ],
    )
    async def kick(self, context: SlashContext, user: discord.User, reason: str = "Not specified"):
        """
        Kick a user out of the server.
        """
        author = await context.guild.fetch_member(context.author_id)
        if not author.guild_permissions.kick_members:
            embed = discord.Embed(
                title="Error!",
                description="You don't have enough permissions to kick this user.",
                color=0xE02B2B
            )
            return await context.send(embed=embed)
        member = await context.guild.fetch_member(user.id)
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                title="Error!",
                description="User has Admin permissions.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
        else:
            try:
                await member.kick(reason=reason)
                embed = discord.Embed(
                    title="User Kicked!",
                    description=f"**{member}** was kicked by **{context.author}**!",
                    color=0x42F56C
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await context.send(embed=embed)
                try:
                    await member.send(
                        f"You were kicked by **{context.author}**!\nReason: {reason}"
                    )
                except:
                    pass
            except:
                embed = discord.Embed(
                    title="Error!",
                    description="An error occurred while trying to kick the user. Make sure my role is above the role of the user you want to kick.",
                    color=0xE02B2B
                )
                await context.message.channel.send(embed=embed)

    @cog_ext.cog_slash(
        name='nick',
        description="Change the nickname of a user on a server.",
        options=[
            create_option(
                name="user",
                description="The user you want to change the nickname.",
                option_type=6,
                required=True
            ),
            create_option(
                name="nickname",
                description="The new nickname of the user.",
                option_type=3,
                required=False
            )
        ],
    )
    async def nick(self, context: SlashContext, user: discord.User, nickname: str = None):
        """
        Change the nickname of a user on a server.
        """
        author = await context.guild.fetch_member(context.author_id)
        if not author.guild_permissions.manage_nicknames:
            embed = discord.Embed(
                title="Error!",
                description="You don't have enough permissions to change the nickname of this user.",
                color=0xE02B2B
            )
            return await context.send(embed=embed)
        member = await context.guild.fetch_member(user.id)
        try:
            await member.edit(nick=nickname)
            embed = discord.Embed(
                title="Changed Nickname!",
                description=f"**{member}'s** new nickname is **{nickname}**!",
                color=0x42F56C
            )
            await context.send(embed=embed)
        except:
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to change the nickname of the user. Make sure my role is above the role of the user you want to change the nickname.",
                color=0xE02B2B
            )
            await context.message.channel.send(embed=embed)

    @cog_ext.cog_slash(
        name='ban',
        description="Bans a user from the server.",
        options=[
            create_option(
                name="user",
                description="The user you want to ban.",
                option_type=6,
                required=True
            ),
            create_option(
                name="reason",
                description="The reason you banned the user.",
                option_type=3,
                required=False
            )
        ],
    )
    async def ban(self, context, user: discord.User, reason: str = "Not specified"):
        """
        Bans a user from the server.
        """
        author = await context.guild.fetch_member(context.author_id)
        if not author.guild_permissions.ban_members:
            embed = discord.Embed(
                title="Error!",
                description="You don't have enough permissions to ban this user.",
                color=0xE02B2B
            )
            return await context.send(embed=embed)
        member = await context.guild.fetch_member(user.id)
        try:
            if member.guild_permissions.administrator:
                embed = discord.Embed(
                    title="Error!",
                    description="User has Admin permissions.",
                    color=0xE02B2B
                )
                await context.send(embed=embed)
            else:
                await member.ban(reason=reason)
                embed = discord.Embed(
                    title="User Banned!",
                    description=f"**{member}** was banned by **{context.author}**!",
                    color=0x42F56C
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await context.send(embed=embed)
                await member.send(f"You were banned by **{context.author}**!\nReason: {reason}")
        except:
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to ban the user. Make sure my role is above the role of the user you want to ban.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @cog_ext.cog_slash(
        name='warn',
        description="Warns a user from the server.",
        options=[
            create_option(
                name="user",
                description="The user you want to warn.",
                option_type=6,
                required=True
            ),
            create_option(
                name="reason",
                description="The reason you warned the user.",
                option_type=3,
                required=False
            )
        ],
    )
    async def warn(self, context, user: discord.User, reason: str = "Not specified"):
        """
        Warns a user in his private messages.
        """
        author = await context.guild.fetch_member(context.author_id)
        if not author.guild_permissions.manage_messages:
            embed = discord.Embed(
                title="Error!",
                description="You don't have enough permissions to warn this user.",
                color=0xE02B2B
            )
            return await context.send(embed=embed)
        member = await context.guild.fetch_member(user.id)
        embed = discord.Embed(
            title="User Warned!",
            description=f"**{member}** was warned by **{context.author}**!",
            color=0x42F56C
        )
        embed.add_field(
            name="Reason:",
            value=reason
        )
        await context.send(embed=embed)
        try:
            await member.send(f"You were warned by **{context.author}**!\nReason: {reason}")
        except:
            pass

    @cog_ext.cog_slash(
        name='purge',
        description="Delete a number of messages.",
        options=[
            create_option(
                name="amount",
                description="The amount of messages you want to delete.",
                option_type=4,
                required=True
            )
        ],
    )
    @commands.has_permissions(manage_messages=True, manage_channels=True)
    async def purge(self, context, amount: int):
        """
        Delete a number of messages.
        """
        author = await context.guild.fetch_member(context.author_id)
        if not author.guild_permissions.manage_messages or not author.guild_permissions.manage_channels:
            embed = discord.Embed(
                title="Error!",
                description="You don't have enough permissions purge the chat.",
                color=0xE02B2B
            )
            return await context.send(embed=embed)
        try:
            amount = int(amount)
        except:
            embed = discord.Embed(
                title="Error!",
                description=f"`{amount}` is not a valid number.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        if amount < 1:
            embed = discord.Embed(
                title="Error!",
                description=f"`{amount}` is not a valid number.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        purged_messages = await context.channel.purge(limit=amount)
        embed = discord.Embed(
            title="Chat Cleared!",
            description=f"**{context.author}** cleared **{len(purged_messages)}** messages!",
            color=0x42F56C
        )
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(moderation(bot))
