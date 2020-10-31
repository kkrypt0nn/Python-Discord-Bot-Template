import os, sys, discord
from discord.ext import commands

if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config


class Help(commands.Cog, name="help"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, context):
        """List all commands from every Cog the bot has loaded."""
        prefix = config.BOT_PREFIX
        if not isinstance(prefix, str):
            prefix = prefix[0]
        embed = discord.Embed(title="Help", description="List of available commands:", color=0x00FF00)
        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            cmds = cog.get_commands()
            command_list = [c.name for c in cmds]
            command_helps = [c.help for c in cmds]
            help_text = '\n'.join(f'{prefix}{n} - {h}' for n, h in zip(command_list, command_helps))
            embed.add_field(name=i.capitalize(), value=f'```{help_text}```', inline=False)
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
