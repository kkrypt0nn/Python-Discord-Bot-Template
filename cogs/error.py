import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
from discord.ext.commands import has_role
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext.commands import cooldown, BucketType

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You Can Not Use This Command.")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("You Can Not Use This Command In A DM.")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("Sorry, DisSlash Does Not Have The Proper Perms To Execute This Command")
        else:
            print(error)

def setup(bot):
    bot.add_cog(Error(bot))
