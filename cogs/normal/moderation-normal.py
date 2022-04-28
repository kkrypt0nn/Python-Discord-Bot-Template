""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""

import disnake
from disnake.ext import commands
from disnake.ext.commands import Context

from helpers import checks


class Moderation(commands.Cog, name="moderation-normal"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="kick",
        description="Kick a user out of the server.",
    )
    @commands.has_permissions(kick_members=True)
    @checks.not_blacklisted()
    async def kick(self, context: Context, member: disnake.Member, *, reason: str = "Not specified") -> None:
        """
        Kick a user out of the server.
        :param context: The context in which the command has been executed.
        :param member: The member that should be kicked from the server.
        :param reason: The reason for the kick. Default is "Not specified".
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

    @commands.command(
        name="nick",
        description="Change the nickname of a user on a server.",
    )
    @commands.has_permissions(manage_nicknames=True)
    @checks.not_blacklisted()
    async def nick(self, context: Context, member: disnake.Member, *, nickname: str = None) -> None:
        """
        Change the nickname of a user on a server.
        :param context: The context in which the command has been executed.
        :param member: The member that should have its nickname changed.
        :param nickname: The new nickname of the user. Default is None, which will reset the nickname.
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

    @commands.command(
        name="ban",
        description="Bans a user from the server.",
    )
    @commands.has_permissions(ban_members=True)
    @checks.not_blacklisted()
    async def ban(self, context: Context, member: disnake.Member, *, reason: str = "Not specified") -> None:
        """
        Bans a user from the server.
        :param context: The context in which the command has been executed.
        :param member: The member that should be banned from the server.
        :param reason: The reason for the ban. Default is "Not specified".
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

    @commands.command(
        name="warn",
        description="Warns a user in the server.",
    )
    @commands.has_permissions(manage_messages=True)
    @checks.not_blacklisted()
    async def warn(self, context: Context, member: disnake.Member, *, reason: str = "Not specified") -> None:
        """
        Warns a user in his private messages.
        :param context: The context in which the command has been executed.
        :param member: The member that should be warned.
        :param reason: The reason for the warn. Default is "Not specified".
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

    @commands.command(
        name="purge",
        description="Delete a number of messages.",
    )
    @commands.has_guild_permissions(manage_messages=True)
    @checks.not_blacklisted()
    async def purge(self, context: Context, amount: int) -> None:
        """
        Delete a number of messages.
        :param context: The context in which the command has been executed.
        :param amount: The number of messages that should be deleted.
        """
        try:
            amount = int(amount)
        except:
            embed = disnake.Embed(
                title="Error!",
                description=f"`{amount}` is not a valid number.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        if amount < 1:
            embed = disnake.Embed(
                title="Error!",
                description=f"`{amount}` is not a valid number.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        purged_messages = await context.channel.purge(limit=amount)
        embed = disnake.Embed(
            title="Chat Cleared!",
            description=f"**{context.author}** cleared **{len(purged_messages)}** messages!",
            color=0x9C84EF
        )
        await context.send(embed=embed)

    @commands.command(
        name="hackban",
        description="Bans a user without the user having to be in the server."
    )
    async def hackban(self, context: Context, user_id: int, *, reason: str) -> None:
        """
        Bans a user without the user having to be in the server.
        :param context: The context in which the command has been executed.
        :param user_id: The ID of the user that should be banned.
        :param reason: The reason for the ban. Default is "Not specified".
        """
        try:
            await self.bot.http.ban(user_id, context.guild.id, reason=reason)
            user = await self.bot.get_or_fetch_user(user_id)
            embed = disnake.Embed(
                title="User Banned!",
                description=f"**{user} (ID: {user_id}) ** was banned by **{context.author}**!",
                color=0x9C84EF
            )
            embed.add_field(
                name="Reason:",
                value=reason
            )
            await context.send(embed=embed)
        except:
            embed = disnake.Embed(
                title="Error!",
                description="An error occurred while trying to ban the user. Make sure ID is an existing ID that belongs to a user.",
                color=0xE02B2B
            )
            await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
