import os, sys, discord
from discord.ext import commands
if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config

class owner(commands.Cog, name="owner"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shutdown")
    async def shutdown(self, context):
        """
        Make the bot shutdown
        """
        if context.message.author.id in config.OWNERS:
            embed = discord.Embed(
                description="Shutting down. Bye! :wave:",
                color=0x00FF00
            )
            await context.send(embed=embed)
            await self.bot.logout()
            await self.bot.close()
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0xFF0000
            )
            await context.send(embed=embed)

    @commands.command(name="say", aliases=["echo"])
    async def say(self, context, *, args):
        """
        The bot will say anything you want.
        """
        if context.message.author.id in config.OWNERS:
            await context.send(args)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0xFF0000
            )
            await context.send(embed=embed)

    @commands.command(name="embed")
    async def embed(self, context, *, args):
        """
        The bot will say anything you want, but within embeds.
        """
        if context.message.author.id in config.OWNERS:
            embed = discord.Embed(
                description=args,
                color=0x00FF00
            )
            await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0xFF0000
            )
            await context.send(embed=embed)

    @commands.group(name="blacklist")
    async def blacklist(self, context):
        """
        Lets you add or remove a user from not being able to use the bot.
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                title=f"There are currently {len(config.BLACKLIST)} blacklisted IDs",
                description=f"{config.BLACKLIST}",
                color=0x0000FF
            )
            await context.send(embed=embed)

    @blacklist.command(name="add")
    async def blacklist_add(self, context, member: discord.Member):
        """
        Lets you add a user from not being able to use the bot.
        """
        if context.message.author.id in config.OWNERS:
            userID = member.id
            try:
                config.BLACKLIST.append(userID)
                embed = discord.Embed(
                    title="User Blacklisted",
                    description=f"**{member.name}** has been successfully added to the blacklist",
                    color=0x00FF00
                )
                embed.set_footer(
                    text=f"There are now {len(config.BLACKLIST)} users in the blacklist"
                )
                await context.send(embed=embed)
            except:
                embed = discord.Embed(
                    title="Error!",
                    description=f"An unknown error occurred when trying to add **{member.name}** to the blacklist.",
                    color=0xFF0000
                )
                await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0xFF0000
            )
            await context.send(embed=embed)

    @blacklist.command(name="remove")
    async def blacklist_remove(self, context, member: discord.Member):
        """
        Lets you remove a user from not being able to use the bot.
        """
        if context.message.author.id in config.OWNERS:
            userID = member.id
            try:
                config.BLACKLIST.remove(userID)
                embed = discord.Embed(
                    title="User Unblacklisted",
                    description=f"**{member.name}** has been successfully removed from the blacklist",
                    color=0x00FF00
                )
                embed.set_footer(
                    text=f"There are now {len(config.BLACKLIST)} users in the blacklist"
                )
                await context.send(embed=embed)
            except:
                embed = discord.Embed(
                    title="Error!",
                    description=f"An unknown error occurred when trying to remove **{member.name}** from the blacklist.",
                    color=0xFF0000
                )
                await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0xFF0000
            )
            await context.send(embed=embed)

def setup(bot):
    bot.add_cog(owner(bot))