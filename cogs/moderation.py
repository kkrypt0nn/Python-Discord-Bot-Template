"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.4.0
"""

import os
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Moderation(commands.Cog, name="moderation"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="kick",
        description="Kick a user out of the server.",
    )
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @app_commands.describe(
        user="The user that should be kicked.",
        reason="The reason why the user should be kicked.",
    )
    async def kick(
        self, context: Context, user: discord.User, *, reason: str = "Not specified"
    ) -> None:
        """
        Kick a user out of the server.

        :param context: The hybrid command context.
        :param user: The user that should be kicked from the server.
        :param reason: The reason for the kick. Default is "Not specified".
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                description="User has administrator permissions.", color=0xE02B2B
            )
            await context.send(embed=embed)
        else:
            try:
                embed = discord.Embed(
                    description=f"**{member}** was kicked by **{context.author}**!",
                    color=0xBEBEFE,
                )
                embed.add_field(name="Reason:", value=reason)
                await context.send(embed=embed)
                try:
                    await member.send(
                        f"You were kicked by **{context.author}** from **{context.guild.name}**!\nReason: {reason}"
                    )
                except:
                    # Couldn't send a message in the private messages of the user
                    pass
                await member.kick(reason=reason)
            except:
                embed = discord.Embed(
                    description="An error occurred while trying to kick the user. Make sure my role is above the role of the user you want to kick.",
                    color=0xE02B2B,
                )
                await context.send(embed=embed)

    @commands.hybrid_command(
        name="nick",
        description="Change the nickname of a user on a server.",
    )
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    @app_commands.describe(
        user="The user that should have a new nickname.",
        nickname="The new nickname that should be set.",
    )
    async def nick(
        self, context: Context, user: discord.User, *, nickname: str = None
    ) -> None:
        """
        Change the nickname of a user on a server.

        :param context: The hybrid command context.
        :param user: The user that should have its nickname changed.
        :param nickname: The new nickname of the user. Default is None, which will reset the nickname.
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        try:
            await member.edit(nick=nickname)
            embed = discord.Embed(
                description=f"**{member}'s** new nickname is **{nickname}**!",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
        except:
            embed = discord.Embed(
                description="An error occurred while trying to change the nickname of the user. Make sure my role is above the role of the user you want to change the nickname.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="ban",
        description="Bans a user from the server.",
    )
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @app_commands.describe(
        user="The user that should be banned.",
        reason="The reason why the user should be banned.",
    )
    async def ban(
        self, context: Context, user: discord.User, *, reason: str = "Not specified"
    ) -> None:
        """
        Bans a user from the server.

        :param context: The hybrid command context.
        :param user: The user that should be banned from the server.
        :param reason: The reason for the ban. Default is "Not specified".
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        try:
            if member.guild_permissions.administrator:
                embed = discord.Embed(
                    description="User has administrator permissions.", color=0xE02B2B
                )
                await context.send(embed=embed)
            else:
                embed = discord.Embed(
                    description=f"**{member}** was banned by **{context.author}**!",
                    color=0xBEBEFE,
                )
                embed.add_field(name="Reason:", value=reason)
                await context.send(embed=embed)
                try:
                    await member.send(
                        f"You were banned by **{context.author}** from **{context.guild.name}**!\nReason: {reason}"
                    )
                except:
                    # Couldn't send a message in the private messages of the user
                    pass
                await member.ban(reason=reason)
        except:
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to ban the user. Make sure my role is above the role of the user you want to ban.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @commands.hybrid_group(
        name="warning",
        description="Manage warnings of a user on a server.",
    )
    @commands.has_permissions(manage_messages=True)
    async def warning(self, context: Context) -> None:
        """
        Manage warnings of a user on a server.

        :param context: The hybrid command context.
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Please specify a subcommand.\n\n**Subcommands:**\n`add` - Add a warning to a user.\n`remove` - Remove a warning from a user.\n`list` - List all warnings of a user.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @warning.command(
        name="add",
        description="Adds a warning to a user in the server.",
    )
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(
        user="The user that should be warned.",
        reason="The reason why the user should be warned.",
    )
    async def warning_add(
        self, context: Context, user: discord.User, *, reason: str = "Not specified"
    ) -> None:
        """
        Warns a user in his private messages.

        :param context: The hybrid command context.
        :param user: The user that should be warned.
        :param reason: The reason for the warn. Default is "Not specified".
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        total = await self.bot.database.add_warn(
            user.id, context.guild.id, context.author.id, reason
        )
        embed = discord.Embed(
            description=f"**{member}** was warned by **{context.author}**!\nTotal warns for this user: {total}",
            color=0xBEBEFE,
        )
        embed.add_field(name="Reason:", value=reason)
        await context.send(embed=embed)
        try:
            await member.send(
                f"You were warned by **{context.author}** in **{context.guild.name}**!\nReason: {reason}"
            )
        except:
            # Couldn't send a message in the private messages of the user
            await context.send(
                f"{member.mention}, you were warned by **{context.author}**!\nReason: {reason}"
            )

    @warning.command(
        name="remove",
        description="Removes a warning from a user in the server.",
    )
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(
        user="The user that should get their warning removed.",
        warn_id="The ID of the warning that should be removed.",
    )
    async def warning_remove(
        self, context: Context, user: discord.User, warn_id: int
    ) -> None:
        """
        Warns a user in his private messages.

        :param context: The hybrid command context.
        :param user: The user that should get their warning removed.
        :param warn_id: The ID of the warning that should be removed.
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        total = await self.bot.database.remove_warn(warn_id, user.id, context.guild.id)
        embed = discord.Embed(
            description=f"I've removed the warning **#{warn_id}** from **{member}**!\nTotal warns for this user: {total}",
            color=0xBEBEFE,
        )
        await context.send(embed=embed)

    @warning.command(
        name="list",
        description="Shows the warnings of a user in the server.",
    )
    @commands.has_guild_permissions(manage_messages=True)
    @app_commands.describe(user="The user you want to get the warnings of.")
    async def warning_list(self, context: Context, user: discord.User) -> None:
        """
        Shows the warnings of a user in the server.

        :param context: The hybrid command context.
        :param user: The user you want to get the warnings of.
        """
        warnings_list = await self.bot.database.get_warnings(user.id, context.guild.id)
        embed = discord.Embed(title=f"Warnings of {user}", color=0xBEBEFE)
        description = ""
        if len(warnings_list) == 0:
            description = "This user has no warnings."
        else:
            for warning in warnings_list:
                description += f"• Warned by <@{warning[2]}>: **{warning[3]}** (<t:{warning[4]}>) - Warn ID #{warning[5]}\n"
        embed.description = description
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="purge",
        description="Delete a number of messages.",
    )
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @app_commands.describe(amount="The amount of messages that should be deleted.")
    async def purge(self, context: Context, amount: int) -> None:
        """
        Delete a number of messages.

        :param context: The hybrid command context.
        :param amount: The number of messages that should be deleted.
        """
        await context.send(
            "Deleting messages..."
        )  # Bit of a hacky way to make sure the bot responds to the interaction and doens't get a "Unknown Interaction" response
        purged_messages = await context.channel.purge(limit=amount + 1)
        embed = discord.Embed(
            description=f"**{context.author}** cleared **{len(purged_messages)-1}** messages!",
            color=0xBEBEFE,
        )
        await context.channel.send(embed=embed)

    @commands.hybrid_command(
        name="hackban",
        description="Bans a user without the user having to be in the server.",
    )
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @app_commands.describe(
        user_id="The user ID that should be banned.",
        reason="The reason why the user should be banned.",
    )
    async def hackban(
        self, context: Context, user_id: str, *, reason: str = "Not specified"
    ) -> None:
        """
        Bans a user without the user having to be in the server.

        :param context: The hybrid command context.
        :param user_id: The ID of the user that should be banned.
        :param reason: The reason for the ban. Default is "Not specified".
        """
        try:
            await self.bot.http.ban(user_id, context.guild.id, reason=reason)
            user = self.bot.get_user(int(user_id)) or await self.bot.fetch_user(
                int(user_id)
            )
            embed = discord.Embed(
                description=f"**{user}** (ID: {user_id}) was banned by **{context.author}**!",
                color=0xBEBEFE,
            )
            embed.add_field(name="Reason:", value=reason)
            await context.send(embed=embed)
        except Exception:
            embed = discord.Embed(
                description="An error occurred while trying to ban the user. Make sure ID is an existing ID that belongs to a user.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="archive",
        description="Archives in a text file the last messages with a chosen limit of messages.",
    )
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(
        limit="The limit of messages that should be archived.",
    )
    async def archive(self, context: Context, limit: int = 10) -> None:
        """
        Archives in a text file the last messages with a chosen limit of messages. This command requires the MESSAGE_CONTENT intent to work properly.

        :param limit: The limit of messages that should be archived. Default is 10.
        """
        log_file = f"{context.channel.id}.log"
        with open(log_file, "w", encoding="UTF-8") as f:
            f.write(
                f'Archived messages from: #{context.channel} ({context.channel.id}) in the guild "{context.guild}" ({context.guild.id}) at {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}\n'
            )
            async for message in context.channel.history(
                limit=limit, before=context.message
            ):
                attachments = []
                for attachment in message.attachments:
                    attachments.append(attachment.url)
                attachments_text = (
                    f"[Attached File{'s' if len(attachments) >= 2 else ''}: {', '.join(attachments)}]"
                    if len(attachments) >= 1
                    else ""
                )
                f.write(
                    f"{message.created_at.strftime('%d.%m.%Y %H:%M:%S')} {message.author} {message.id}: {message.clean_content} {attachments_text}\n"
                )
        f = discord.File(log_file)
        await context.send(file=f)
        os.remove(log_file)


async def setup(bot) -> None:
    await bot.add_cog(Moderation(bot))
