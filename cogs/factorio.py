import asyncio
from datetime import datetime, timedelta, timezone
from typing import Callable, Optional, TypeVar

import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ext.commands import Context

import util.factorio as factorio
from util.util import format_timedelta

JST = timezone(timedelta(hours=+9), 'JST')
T = TypeVar("T")


class FactorioUnavailable(Exception):
    """Factorioサーバに接続できない（停止中・通信エラー）ことを表す例外"""


class Factorio(commands.Cog, name="factorio"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.notice_done_user_dict: dict = {}
        self.rcon_client = None
        self.channel: Optional[discord.abc.Messageable] = None
        # RCONクライアントはスレッドセーフではないため、同時に1つの処理だけが使うようにする
        self.rcon_lock = asyncio.Lock()
        # サーバ到達可否の直前の状態（None=未確認）。状態が変わったときだけログを出すために使う
        self.server_available: Optional[bool] = None
        # 通知開始後、最初に疎通できたかどうか（「既に勤務中」通知を1回だけ出すため）
        self.initial_check_done = False
        self.use_factorio_notice = bool(bot.config["factorio"]["use"])
        # 起動時にはRCON接続しない。サーバが停止していてもCog自体は読み込まれ、
        # 通知ループが接続できるまで再試行する。
        if self.use_factorio_notice:
            self.check_online_user.start()

    def cog_unload(self):
        self.check_online_user.cancel()
        self._close_client()

    def _close_client(self) -> None:
        if self.rcon_client is not None:
            try:
                self.rcon_client.close()
            except Exception:
                pass
        self.rcon_client = None

    def _connect_and_call(self, func: Callable[..., T]) -> T:
        """
        （別スレッドで実行）必要なら接続してから func(client) を呼び出す。
        """
        if self.rcon_client is None:
            client = factorio.create_client(self.bot)
            client.connect()
            self.rcon_client = client
        return func(self.rcon_client)

    async def rcon(self, func: Callable[..., T]) -> T:
        """
        RCON呼び出しを別スレッドで実行し、イベントループ（Bot全体）を止めないようにする。
        失敗した場合は接続を破棄して FactorioUnavailable を送出する（次回呼び出し時に再接続する）。
        """
        async with self.rcon_lock:
            try:
                result = await asyncio.to_thread(self._connect_and_call, func)
            except Exception as e:
                self._close_client()
                self._mark_server(False, e)
                raise FactorioUnavailable(str(e)) from e
            self._mark_server(True)
            return result

    def _mark_server(self, available: bool, error: Optional[Exception] = None) -> None:
        """サーバ到達可否が変化したときだけログを出す"""
        if self.server_available == available:
            return
        self.server_available = available
        if available:
            self.bot.logger.info("[factorio] サーバに接続しました。")
        else:
            self.bot.logger.warning(
                f"[factorio] サーバに接続できません（停止中の可能性）: {type(error).__name__}: {error}"
            )

    async def send_notice(self, *args, **kwargs) -> None:
        if self.channel is None:
            self.bot.logger.warning("[factorio] 通知先チャンネルが見つからないため通知をスキップしました。")
            return
        await self.channel.send(*args, **kwargs)

    @tasks.loop(seconds=5)
    async def check_online_user(self):
        self.bot.logger.debug("[factorio] check_online_user実行開始")
        try:
            online_user_list: list = await self.rcon(factorio.online_player_list)
        except FactorioUnavailable:
            # サーバ停止中・通信エラー時は何もせず次回に再試行する（ループは止めない）
            return
        now: datetime = datetime.now(JST)

        if not self.initial_check_done:
            # 通知開始後、初めて疎通できた時点でオンラインのユーザを通知
            self.initial_check_done = True
            if online_user_list:
                message = ""
                for user_name in online_user_list:
                    self.notice_done_user_dict[user_name] = now
                    message += "「" + user_name + "さん」"
                message += "は既に勤務中です。"
                self.bot.logger.info("[factorio] " + message)
                await self.send_notice(message)
            return

        for user_name in online_user_list:
            if user_name in self.notice_done_user_dict:
                # 通知済みリストにいる = 既知のログイン
                self.bot.logger.debug("[factorio] 「" + user_name + "さん」はログイン通知済み")
                continue
            # 通知済みリストにいない = 新規ログイン
            self.notice_done_user_dict[user_name] = now
            embed = discord.Embed(
                title='勤怠通知',
                description=f"「{user_name}」さんが出勤しました。", color=0xBEBEFE
            )
            self.bot.logger.info("[factorio] " + user_name + "さんがログインしました。")
            await self.send_notice(embed=embed)

        # 通知済みリストにいるのに、オンラインユーザにいない = 新規ログアウト
        for user_name in set(self.notice_done_user_dict) - set(online_user_list):
            login_time: datetime = self.notice_done_user_dict.pop(user_name)
            embed = discord.Embed(
                title='勤怠通知',
                description=f"「{user_name}」さんが退勤しました。", color=0xBEBEFE
            )
            embed.add_field(
                name="今回のプレイ時間:",
                value=f"{format_timedelta(now - login_time)}",
                inline=False,
            )
            self.bot.logger.info("[factorio] " + user_name + "さんがログアウトしました。")
            await self.send_notice(embed=embed)
        self.bot.logger.debug("[factorio] check_online_user実行終了")

    @check_online_user.before_loop
    async def before_check_online_user(self):
        await self.bot.wait_until_ready()
        self.channel = self.bot.get_channel(self.bot.config["factorio"]["notice_channel"])
        if self.channel is None:
            self.bot.logger.warning("[factorio] config.json の notice_channel が見つかりません。")

    @check_online_user.error
    async def on_check_online_user_error(self, error: BaseException) -> None:
        # 想定外の例外でループが止まった場合も記録し、30秒後に再起動する。
        # このハンドラはループのタスク内で呼ばれる（まだ is_running() が True）ため、
        # タスク終了後に別タスクから起動し直す。
        self.bot.logger.error(f"[factorio] 通知ループで想定外のエラー: {type(error).__name__}: {error}")
        self._restart_task = asyncio.create_task(self._restart_loop_later(30))

    async def _restart_loop_later(self, delay: float) -> None:
        await asyncio.sleep(delay)
        if self.use_factorio_notice and not self.check_online_user.is_running():
            self.bot.logger.info("[factorio] 通知ループを再起動します。")
            self.check_online_user.start()

    @commands.hybrid_command(
        name="factorio_notice_stop",
        description="Factorio入退出通知をストップする",
    )
    async def factorio_notice_stop(self, context: Context) -> None:
        """
        Factorioの入退出通知をストップします

        :param context: ハイブリッドコマンドコンテキスト
        """
        if not self.use_factorio_notice:
            # すでに停止済み
            embed = discord.Embed(
                description="Factorio入退室通知機能は起動していませんでした", color=0xE02B2B
            )
            await context.send(embed=embed)
            return

        # 停止させる
        self.use_factorio_notice = False
        self.check_online_user.cancel()
        self.notice_done_user_dict.clear()
        embed = discord.Embed(
            description="Factorio入退室通知機能を停止しました。", color=0xBEBEFE
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="factorio_notice_start",
        description="Factorio入退出通知を起動する",
    )
    async def factorio_notice_start(self, context: Context) -> None:
        """
        Factorioの入退出通知を起動します

        :param context: ハイブリッドコマンドコンテキスト
        """
        if self.use_factorio_notice:
            # すでに起動済み
            embed = discord.Embed(
                description="Factorio入退室通知機能は起動済みです", color=0xE02B2B
            )
            await context.send(embed=embed)
            return

        # 起動させる（接続は通知ループ内で行い、サーバ停止中でも再試行し続ける）
        self.use_factorio_notice = True
        self.initial_check_done = False
        self.check_online_user.start()
        message = "Factorio入退室通知機能を起動しました。"
        if self.server_available is False:
            message += "\n（現在サーバに接続できません。接続できるまで自動で再試行します）"
        embed = discord.Embed(description=message, color=0xBEBEFE)
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="factorio_status",
        description="Factorioステータス取得",
    )
    @app_commands.describe(show_players="プレイヤー情報を表示するか否か(True/False)")
    async def factorio_status(self, context: Context, *, show_players: bool=False) -> None:
        """
        Factorioステータスを確認する

        :param context: ハイブリッドコマンドコンテキスト
        """
        # RCON通信に時間がかかる場合に備え、スラッシュコマンドの応答期限（3秒）を延長する
        await context.defer()
        try:
            seed = await self.rcon(factorio.seed)
            game_time = await self.rcon(factorio.time)
            evolution = await self.rcon(factorio.evolution)
            online_player_list = await self.rcon(factorio.online_player_list)
            player_list = await self.rcon(factorio.player_list)
            version = await self.rcon(factorio.version)
        except FactorioUnavailable:
            embed = discord.Embed(
                description="Factorioサーバに接続できません（停止中の可能性があります）。",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return

        embed = discord.Embed(
            title="Factorioサーバ情報", color=0xBEBEFE
        )
        ## サーバシード値
        embed.add_field(name="シード値:", value=f"{seed}", inline=True)
        ## サーバ内経過時間
        embed.add_field(name="サーバ内経過時間:", value=f"{game_time}", inline=True)
        ## エイリアン進化ファクター
        embed.add_field(name="エイリアン進化ファクター:", value=f"{evolution}", inline=False)
        ## オンラインプレイヤー情報
        self.bot.logger.debug("[factorio] online_player_list:" + str(online_player_list))
        embed.add_field(
            name="現在オンラインユーザ数:",
            value=f"{len(online_player_list)} 人",
            inline=True,
        )
        if show_players:
            embed.add_field(
                name="現在オンラインのユーザ:",
                value=", ".join(online_player_list) or "-",
                inline=False,
            )
        ## 参加ユーザ情報
        self.bot.logger.debug("[factorio] player_list:" + str(player_list))
        embed.add_field(
            name="参加ユーザ数:",
            value=f"{len(player_list)} 人",
            inline=True,
        )
        if show_players:
            embed.add_field(
                name="参加ユーザ:",
                value=", ".join(player_list) or "-",
                inline=False,
            )
        embed.set_footer(text=f"Factorio_version: {version}")
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Factorio(bot))
