""""
Copyright © Krypton 2021 - https://github.com/kkrypt0nn (https://krypt0n.co.uk)
Description:
This is a template to create your own discord bot in python.

Version: 4.0.1
"""

import json
import os
import random
import sys

import aiohttp
import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Context

from helpers import checks

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class Choice(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.choice = None

    @disnake.ui.button(label="Heads", style=disnake.ButtonStyle.blurple)
    async def confirm(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.lower()
        self.stop()

    @disnake.ui.button(label="Tails", style=disnake.ButtonStyle.blurple)
    async def cancel(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.lower()
        self.stop()


class RockPaperScissors(disnake.ui.Select):
    def __init__(self):

        options = [
            disnake.SelectOption(
                label="Scissors", description="You choose scissors.", emoji="🪨"
            ),
            disnake.SelectOption(
                label="Rock", description="You choose rock.", emoji="🧻"
            ),
            disnake.SelectOption(
                label="paper", description="You choose paper.", emoji="✂"
            ),
        ]

        super().__init__(
            placeholder="Choose...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        choices = {
            "rock": 0,
            "paper": 1,
            "scissors": 2,
        }
        user_choice = self.values[0].lower()
        user_choice_index = choices[user_choice]

        bot_choice = random.choice(list(choices.keys()))
        bot_choice_index = choices[bot_choice]

        result_embed = disnake.Embed(color=0x9C84EF)
        result_embed.set_author(name=interaction.author.display_name, icon_url=interaction.author.avatar.url)

        if user_choice_index == bot_choice_index:
            result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0xF59E42
        elif user_choice_index == 0 and bot_choice_index == 2:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x9C84EF
        elif user_choice_index == 1 and bot_choice_index == 0:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x9C84EF
        elif user_choice_index == 2 and bot_choice_index == 1:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x9C84EF
        else:
            result_embed.description = f"**I won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0xE02B2B
        await interaction.response.defer()
        await interaction.edit_original_message(embed=result_embed, content=None, view=None)


class RockPaperScissorsView(disnake.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(RockPaperScissors())


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="randomfact",
        description="Get a random fact."
    )
    @checks.not_blacklisted()
    async def randomfact(self, interaction: ApplicationCommandInteraction):
        """
        Get a random fact.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = disnake.Embed(
                        description=data["text"],
                        color=0xD75BF4
                    )
                else:
                    embed = disnake.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                await interaction.send(embed=embed)

    @commands.command(
        name="randomfact",
        description="Get a random fact."
    )
    @checks.not_blacklisted()
    async def randomfact(self, context: Context):
        """
        Get a random fact.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = disnake.Embed(
                        description=data["text"],
                        color=0xD75BF4
                    )
                else:
                    embed = disnake.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                await context.send(embed=embed)

    @commands.slash_command(
        name="coinflip",
        description="Make a coin flip, but give your bet before."
    )
    @checks.not_blacklisted()
    async def coinflip(self, interaction: ApplicationCommandInteraction):
        buttons = Choice()
        embed = disnake.Embed(
            description="What is your bet?",
            color=0x9C84EF
        )
        await interaction.send(embed=embed, view=buttons)
        await buttons.wait()  # We wait for the user to click a button.
        result = random.choice(["heads", "tails"])
        if buttons.choice == result:
            # User guessed correctly
            embed = disnake.Embed(
                description=f"Correct! You guessed `{buttons.choice}` and I flipped the coin to `{result}`.",
                color=0x9C84EF
            )
        else:
            embed = disnake.Embed(
                description=f"Woops! You guessed `{buttons.choice}` and I flipped the coin to `{result}`, better luck next time!",
                color=0xE02B2B
            )
        await interaction.edit_original_message(embed=embed, view=None)

    @commands.command(
        name="coinflip",
        description="Make a coin flip, but give your bet before."
    )
    @checks.not_blacklisted()
    async def coinflip(self, context: Context):
        buttons = Choice()
        embed = disnake.Embed(
            description="What is your bet?",
            color=0x9C84EF
        )
        message = await context.send(embed=embed, view=buttons)
        await buttons.wait()  # We wait for the user to click a button.
        result = random.choice(["heads", "tails"])
        if buttons.choice == result:
            # User guessed correctly
            embed = disnake.Embed(
                description=f"Correct! You guessed `{buttons.choice}` and I flipped the coin to `{result}`.",
                color=0x9C84EF
            )
        else:
            embed = disnake.Embed(
                description=f"Woops! You guessed `{buttons.choice}` and I flipped the coin to `{result}`, better luck next time!",
                color=0xE02B2B
            )
        await message.edit(embed=embed, view=None)

    @commands.slash_command(
        name="rps",
        description="Play the rock paper scissors against the bot."
    )
    @checks.not_blacklisted()
    async def rock_paper_scissors(self, interaction: ApplicationCommandInteraction):
        view = RockPaperScissorsView()
        await interaction.send("Please make your choice", view=view)

    @commands.command(
        name="rps",
        description="Play the rock paper scissors against the bot."
    )
    @checks.not_blacklisted()
    async def rock_paper_scissors(self, context: Context):
        view = RockPaperScissorsView()
        await context.send("Please make your choice", view=view)


def setup(bot):
    bot.add_cog(Fun(bot))
