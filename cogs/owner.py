"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.6.0
"""

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Owner(commands.Cog, name="owner"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(
        name="sync",
        description="スラッシュコマンドを同期します",
    )
    @app_commands.describe(scope="同期対象のスコープを入力してください。(global or guild)")
    @commands.is_owner()
    async def sync(self, context: Context, scope: str) -> None:
        """
        スラッシュコマンドを同期する

        :param context: コマンドコンテキスト
        :param scope: 同期対象のスコープ(global or guild)
        """

        if scope == "global":
            await context.bot.tree.sync()
            embed = discord.Embed(
                description="スラッシュコマンドがグローバルに同期されました",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        elif scope == "guild":
            context.bot.tree.copy_global_to(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                description="スラッシュコマンドがギルドに同期されました",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description="指定するスコープは「global」又は「guild」である必要があります。", color=0xE02B2B
        )
        await context.send(embed=embed)

    @commands.command(
        name="unsync",
        description="スラッシュコマンドをクリアします。",
    )
    @app_commands.describe(
        scope="クリアする対象のスコープを入力してください。(global or guild)"
    )
    @commands.is_owner()
    async def unsync(self, context: Context, scope: str) -> None:
        """
        スラッシュコマンドをクリアする。

        :param context: コマンドコンテキスト
        :param scope: クリア対象のスコープ(global or guild)
        """

        if scope == "global":
            context.bot.tree.clear_commands(guild=None)
            await context.bot.tree.sync()
            embed = discord.Embed(
                description="スラッシュコマンドがグローバルからクリアされました。",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        elif scope == "guild":
            context.bot.tree.clear_commands(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                description="スラッシュコマンドがこのギルドからクリアされました",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description="scopeは「global」又は「guild」を指定してください", color=0xE02B2B
        )
        await context.send(embed=embed)

    @commands.command(
        name="load",
        description="特定のcogを読み込みます",
    )
    @app_commands.describe(cog="読み込むcogの名前")
    @commands.is_owner()
    async def load(self, context: Context, cog: str) -> None:
        """
        botに指定したcogを読み込む

        :param context: ハイブリッドコマンドコンテキスト
        :param cog: 読み込むcogの名前
        """
        try:
            await self.bot.load_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"`{cog}` cogを読み込むことができませんでした。", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"`{cog}` cogの読み込みに成功しました。", color=0xBEBEFE
        )
        await context.send(embed=embed)

    @commands.command(
        name="unload",
        description="特定のcogをアンロードします",
    )
    @app_commands.describe(cog="アンロードするcogの名前")
    @commands.is_owner()
    async def unload(self, context: Context, cog: str) -> None:
        """
        botから指定したcogをアンロードする

        :param context: ハイブリッドコマンドコンテキスト
        :param cog: アンロードするcogの名前
        """
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"`{cog}` cogのアンロードに失敗しました。", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"`{cog}` cogのアンロードに成功しました。", color=0xBEBEFE
        )
        await context.send(embed=embed)

    @commands.command(
        name="reload",
        description="特定のcogをリロードする",
    )
    @app_commands.describe(cog="リロードするcogの名前")
    @commands.is_owner()
    async def reload(self, context: Context, cog: str) -> None:
        """
        botから指定したcogをリロードする

        :param context: ハイブリッドコマンドコンテキスト
        :param cog: リロードする対象のcogファイル名
        """
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"Could not reload the `{cog}` cog.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"Successfully reloaded the `{cog}` cog.", color=0xBEBEFE
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="shutdown",
        description="Botを停止させる",
    )
    @commands.is_owner()
    async def shutdown(self, context: Context) -> None:
        """
        Botを停止させる

        :param context: ハイブリッドコマンドコンテキスト
        """
        embed = discord.Embed(description="Shutting down. Bye! :wave:", color=0xBEBEFE)
        await context.send(embed=embed)
        await self.bot.close()

    @commands.hybrid_command(
        name="say",
        description="Botに指定した文言を発言させる",
    )
    @app_commands.describe(message="Botに発言させるメッセージ")
    @commands.is_owner()
    async def say(self, context: Context, *, message: str) -> None:
        """
        Botはあなたの望むことを何でも言う。

        :param context: ハイブリッドコマンドコンテキスト
        :param message: Botに発言させるメッセージ
        """
        await context.send(message)

    @commands.hybrid_command(
        name="say_embed",
        description="Botに指定した文言を埋め込み形式で発現させる",
    )
    @app_commands.describe(message="Botに発現させるメッセージ")
    @commands.is_owner()
    async def embed(self, context: Context, *, message: str) -> None:
        """
        Botに指定した文言を埋め込み形式で発現させる

        :param context: ハイブリッドコマンドコンテキスト
        :param message: Botに発現させるメッセージ
        """
        embed = discord.Embed(description=message, color=0xBEBEFE)
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Owner(bot))
