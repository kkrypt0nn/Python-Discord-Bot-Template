""""
Copyright © Krypton 2021 - https://github.com/kkrypt0nn (https://krypt0n.co.uk)
Description:
This is a template to create your own discord bot in python.

Version: 4.0.1
"""

import json
import os
import sys

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands
from disnake.ext.commands import Context

from helpers import checks

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class Moderation(commands.Cog, name="moderation"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='kick',
        description="Kick a user out of the server.",
        options=[
            Option(
                name="user",
                description="The user you want to kick.",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="reason",
                description="The reason you kicked the user.",
                type=OptionType.string,
                required=False
            )
        ]
    )
    @commands.has_permissions(kick_members=True)
    @checks.not_blacklisted()
    async def kick(self, interaction: ApplicationCommandInteraction, user: disnake.User, reason: str = "Not specified"):
        """
        Kick a user out of the server.
        """
        member = interaction.guild.get_member(user.id) or await interaction.guild.fetch_member(user.id)
        if member.guild_permissions.administrator:
            embed = disnake.Embed(
                title="Error!",
                description="User has Admin permissions.",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)
        else:
            try:
                embed = disnake.Embed(
                    title="User Kicked!",
                    description=f"**{member}** was kicked by **{interaction.author}**!",
                    color=0x9C84EF
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await interaction.send(embed=embed)
                try:
                    await member.send(
                        f"You were kicked by **{interaction.author}**!\nReason: {reason}"
                    )
                except disnake.Forbidden:
                    # Couldn't send a message in the private messages of the user
                    pass
                await member.kick(reason=reason)
            except:
                embed = disnake.Embed(
                    title="Error!",
                    description="An error occurred while trying to kick the user. Make sure my role is above the role of the user you want to kick.",
                    color=0xE02B2B
                )
                await interaction.send(embed=embed)

    @commands.command(
        name='kick',
        description="Kick a user out of the server.",
    )
    @commands.has_permissions(kick_members=True)
    @checks.not_blacklisted()
    async def kick(self, context: Context, member: disnake.Member, *, reason: str = "Not specified"):
        """
        Kick a user out of the server.
        """
        if member.guild_permissions.administrator:
            embed = disnake.Embed(
                title="Error!",
                description="User has Admin permissions.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
        else:
            try:
                embed = disnake.Embed(
                    title="User Kicked!",
                    description=f"**{member}** was kicked by **{context.author}**!",
                    color=0x9C84EF
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
                except disnake.Forbidden:
                    # Couldn't send a message in the private messages of the user
                    pass
                await member.kick(reason=reason)
            except:
                embed = disnake.Embed(
                    title="Error!",
                    description="An error occurred while trying to kick the user. Make sure my role is above the role of the user you want to kick.",
                    color=0xE02B2B
                )
                await context.send(embed=embed)

    @commands.slash_command(
        name='nick',
        description="Change the nickname of a user on a server.",
        options=[
            Option(
                name="user",
                description="The user you want to change the nickname.",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="nickname",
                description="The new nickname of the user.",
                type=OptionType.string,
                required=False
            )
        ],
    )
    @commands.has_permissions(manage_nicknames=True)
    @checks.not_blacklisted()
    async def nick(self, interaction: ApplicationCommandInteraction, user: disnake.User, nickname: str = None):
        """
        Change the nickname of a user on a server.
        """
        member = interaction.guild.get_member(user.id) or await interaction.guild.fetch_member(user.id)
        try:
            await member.edit(nick=nickname)
            embed = disnake.Embed(
                title="Changed Nickname!",
                description=f"**{member}'s** new nickname is **{nickname}**!",
                color=0x9C84EF
            )
            await interaction.send(embed=embed)
        except:
            embed = disnake.Embed(
                title="Error!",
                description="An error occurred while trying to change the nickname of the user. Make sure my role is above the role of the user you want to change the nickname.",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)

    @commands.command(
        name='nick',
        description="Change the nickname of a user on a server.",
    )
    @commands.has_permissions(manage_nicknames=True)
    @checks.not_blacklisted()
    async def nick(self, context: Context, member: disnake.Member, *, nickname: str = None):
        """
        Change the nickname of a user on a server.
        """
        try:
            await member.edit(nick=nickname)
            embed = disnake.Embed(
                title="Changed Nickname!",
                description=f"**{member}'s** new nickname is **{nickname}**!",
                color=0x9C84EF
            )
            await context.send(embed=embed)
        except:
            embed = disnake.Embed(
                title="Error!",
                description="An error occurred while trying to change the nickname of the user. Make sure my role is above the role of the user you want to change the nickname.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @commands.slash_command(
        name='ban',
        description="Bans a user from the server.",
        options=[
            Option(
                name="user",
                description="The user you want to ban.",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="reason",
                description="The reason you banned the user.",
                type=OptionType.string,
                required=False
            )
        ],
    )
    @commands.has_permissions(ban_members=True)
    @checks.not_blacklisted()
    async def ban(self, interaction: ApplicationCommandInteraction, user: disnake.User, reason: str = "Not specified"):
        """
        Bans a user from the server.
        """
        member = interaction.guild.get_member(user.id) or await interaction.guild.fetch_member(user.id)
        try:
            if member.guild_permissions.administrator:
                embed = disnake.Embed(
                    title="Error!",
                    description="User has Admin permissions.",
                    color=0xE02B2B
                )
                await interaction.send(embed=embed)
            else:
                embed = disnake.Embed(
                    title="User Banned!",
                    description=f"**{member}** was banned by **{interaction.author}**!",
                    color=0x9C84EF
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await interaction.send(embed=embed)
                try:
                    await member.send(f"You were banned by **{interaction.author}**!\nReason: {reason}")
                except disnake.Forbidden:
                    # Couldn't send a message in the private messages of the user
                    pass
                await member.ban(reason=reason)
        except:
            embed = disnake.Embed(
                title="Error!",
                description="An error occurred while trying to ban the user. Make sure my role is above the role of the user you want to ban.",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)

    @commands.command(
        name='ban',
        description="Bans a user from the server.",
    )
    @commands.has_permissions(ban_members=True)
    @checks.not_blacklisted()
    async def ban(self, context: Context, member: disnake.Member, *, reason: str = "Not specified"):
        """
        Bans a user from the server.
        """
        try:
            if member.guild_permissions.administrator:
                embed = disnake.Embed(
                    title="Error!",
                    description="User has Admin permissions.",
                    color=0xE02B2B
                )
                await context.send(embed=embed)
            else:
                embed = disnake.Embed(
                    title="User Banned!",
                    description=f"**{member}** was banned by **{context.author}**!",
                    color=0x9C84EF
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await context.send(embed=embed)
                try:
                    await member.send(f"You were banned by **{context.author}**!\nReason: {reason}")
                except disnake.Forbidden:
                    # Couldn't send a message in the private messages of the user
                    pass
                await member.ban(reason=reason)
        except:
            embed = disnake.Embed(
                title="Error!",
                description="An error occurred while trying to ban the user. Make sure my role is above the role of the user you want to ban.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @commands.slash_command(
        name='warn',
        description="Warns a user in the server.",
        options=[
            Option(
                name="user",
                description="The user you want to warn.",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="reason",
                description="The reason you warned the user.",
                type=OptionType.string,
                required=False
            )
        ],
    )
    @commands.has_permissions(manage_messages=True)
    @checks.not_blacklisted()
    async def warn(self, interaction: ApplicationCommandInteraction, user: disnake.User, reason: str = "Not specified"):
        """
        Warns a user in his private messages.
        """
        member = interaction.guild.get_member(user.id) or await interaction.guild.fetch_member(user.id)
        embed = disnake.Embed(
            title="User Warned!",
            description=f"**{member}** was warned by **{interaction.author}**!",
            color=0x9C84EF
        )
        embed.add_field(
            name="Reason:",
            value=reason
        )
        await interaction.send(embed=embed)
        try:
            await member.send(f"You were warned by **{interaction.author}**!\nReason: {reason}")
        except disnake.Forbidden:
            # Couldn't send a message in the private messages of the user
            await interaction.send(f"{member.mention}, you were warned by **{interaction.author}**!\nReason: {reason}")

    @commands.command(
        name='warn',
        description="Warns a user in the server.",
    )
    @commands.has_permissions(manage_messages=True)
    @checks.not_blacklisted()
    async def warn(self, context: Context, member: disnake.Member, *, reason: str = "Not specified"):
        """
        Warns a user in his private messages.
        """
        embed = disnake.Embed(
            title="User Warned!",
            description=f"**{member}** was warned by **{context.author}**!",
            color=0x9C84EF
        )
        embed.add_field(
            name="Reason:",
            value=reason
        )
        await context.send(embed=embed)
        try:
            await member.send(f"You were warned by **{context.author}**!\nReason: {reason}")
        except disnake.Forbidden:
            # Couldn't send a message in the private messages of the user
            await context.send(f"{member.mention}, you were warned by **{context.author}**!\nReason: {reason}")

    @commands.slash_command(
        name='purge',
        description="Delete a number of messages.",
        options=[
            Option(
                name="amount",
                description="The amount of messages you want to delete. (Must be between 1 and 100.)",
                type=OptionType.integer,
                required=True,
                min_value=1,
                max_value=100
            )
        ],
    )
    @commands.has_guild_permissions(manage_messages=True)
    @checks.not_blacklisted()
    async def purge(self, interaction: ApplicationCommandInteraction, amount: int):
        """
        Delete a number of messages.
        """
        purged_messages = await interaction.channel.purge(limit=amount)
        embed = disnake.Embed(
            title="Chat Cleared!",
            description=f"**{interaction.author}** cleared **{len(purged_messages)}** messages!",
            color=0x9C84EF
        )
        await interaction.send(embed=embed)

    @commands.command(
        name='purge',
        description="Delete a number of messages.",
    )
    @commands.has_guild_permissions(manage_messages=True)
    @checks.not_blacklisted()
    async def purge(self, context: Context, amount: int):
        """
        Delete a number of messages.
        """
        try:
            amount = int(amount)
        except:
            embed = disnake.Embed(
                title="Error!",
                description=f"`{amount}` is not a valid number.",
                color=0xE02B2B
            )
            return await context.send(embed=embed)
        if amount < 1:
            embed = disnake.Embed(
                title="Error!",
                description=f"`{amount}` is not a valid number.",
                color=0xE02B2B
            )
            return await context.send(embed=embed)
        purged_messages = await context.channel.purge(limit=amount)
        embed = disnake.Embed(
            title="Chat Cleared!",
            description=f"**{context.author}** cleared **{len(purged_messages)}** messages!",
            color=0x9C84EF
        )
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
