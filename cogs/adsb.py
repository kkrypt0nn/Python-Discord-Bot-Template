"""
ADS-B 受信機（readsb / tar1090）の aircraft.json を定期的に読み、
軍用機・政府機や、緊急の信号を出している機体が来たら Discord に通知する。

config.json の例:
  "adsb": {
    "use": true,
    "url": "http://<受信機のIP>:8080/data/aircraft.json",
    "map_url": "http://<受信機のIP>:8080/",
    "notice_channel": 123456789012345678,
    "interval_sec": 10,
    "renotify_hours": 6
  }
"adsb" がない、または use が false のときは何もしない。
"""
import asyncio
import time
from typing import Optional

import aiohttp
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context

import util.adsb as adsb


class Adsb(commands.Cog, name="adsb"):
    def __init__(self, bot) -> None:
        self.bot = bot
        conf: dict = bot.config.get("adsb") or {}
        self.use = bool(conf.get("use", False))
        self.url: str = conf.get("url", "")
        self.map_url: str = conf.get("map_url", "")
        self.channel_id = conf.get("notice_channel")
        self.gov_pattern: str = conf.get("gov_pattern", adsb.DEFAULT_GOV_PATTERN)
        self.notifier = adsb.Notifier(float(conf.get("renotify_hours", 6)) * 3600)
        self.channel: Optional[discord.abc.Messageable] = None
        self.session: Optional[aiohttp.ClientSession] = None
        # 受信機に届くかの直前の状態（None=未確認）。変わったときだけログを出す
        self.receiver_ok: Optional[bool] = None
        self.last_aircraft: list = []
        if self.use and self.url:
            self.poll.change_interval(seconds=float(conf.get("interval_sec", 10)))
            self.poll.start()

    async def cog_unload(self) -> None:
        self.poll.cancel()
        if self.session is not None:
            await self.session.close()

    def _mark_receiver(self, ok: bool, error: Optional[Exception] = None) -> None:
        if self.receiver_ok == ok:
            return
        self.receiver_ok = ok
        if ok:
            self.bot.logger.info("[adsb] 受信機からデータを取得できました。")
        else:
            self.bot.logger.warning(f"[adsb] 受信機からデータを取得できません: {type(error).__name__}: {error}")

    async def fetch(self) -> Optional[list]:
        if self.session is None:
            self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5))
        try:
            async with self.session.get(self.url) as resp:
                resp.raise_for_status()
                data = await resp.json(content_type=None)
        except Exception as e:
            self._mark_receiver(False, e)
            return None
        self._mark_receiver(True)
        return data.get("aircraft") or []

    def build_embed(self, det: adsb.Detection) -> discord.Embed:
        ac = det.aircraft
        name = ac.get("r") or (ac.get("flight") or "").strip() or det.hex
        if det.kind == adsb.EMERGENCY:
            title, color = f"緊急の信号を出している機体: {name}", 0xE02B2B
        else:
            title, color = f"軍用機・政府機が近くにいます: {name}", 0x5B7553
        embed = discord.Embed(
            title=title,
            description=det.reason,
            url=f"https://globe.adsbexchange.com/?icao={det.hex}",
            color=color,
        )
        for key, value in adsb.describe(ac).items():
            embed.add_field(name=key, value=value, inline=True)
        if self.map_url:
            embed.add_field(name="家の受信機の地図", value=f"{self.map_url}?icao={det.hex}", inline=False)
        embed.set_footer(text=f"ICAO {det.hex}")
        return embed

    @tasks.loop(seconds=10)
    async def poll(self) -> None:
        aircraft = await self.fetch()
        if aircraft is None:
            return
        self.last_aircraft = aircraft
        now = time.time()
        for det in adsb.detect(aircraft, self.gov_pattern):
            if not self.notifier.should_notify(det, now):
                continue
            self.bot.logger.info(f"[adsb] 通知: {det.hex} {det.kind} {det.reason} {det.aircraft.get('r')}")
            if self.channel is None:
                self.bot.logger.warning("[adsb] 通知先チャンネルが見つからないため通知をスキップしました。")
                continue
            await self.channel.send(embed=self.build_embed(det))
        self.notifier.forget_older_than(now)

    @poll.before_loop
    async def before_poll(self) -> None:
        await self.bot.wait_until_ready()
        self.channel = self.bot.get_channel(self.channel_id) if self.channel_id else None
        if self.channel is None:
            self.bot.logger.warning("[adsb] config.json の adsb.notice_channel が見つかりません。")

    @poll.error
    async def on_poll_error(self, error: BaseException) -> None:
        # 想定外の例外でループが止まったら記録し、30秒後に起動し直す
        self.bot.logger.error(f"[adsb] 通知ループで想定外のエラー: {type(error).__name__}: {error}")
        asyncio.get_running_loop().call_later(30, self._restart)

    def _restart(self) -> None:
        if self.use and not self.poll.is_running():
            self.bot.logger.info("[adsb] 通知ループを再起動します。")
            self.poll.start()

    @commands.hybrid_command(name="adsb_status", description="家の ADS-B 受信機で今見えている飛行機")
    async def adsb_status(self, context: Context) -> None:
        """家の ADS-B 受信機で今見えている飛行機の数と、いちばん近い機体を表示します"""
        if not self.use:
            await context.send(embed=discord.Embed(description="ADS-B の通知は設定されていません。", color=0xE02B2B))
            return
        aircraft = [a for a in self.last_aircraft if float(a.get("seen") or 0) <= 60]
        with_pos = [a for a in aircraft if a.get("r_dst") is not None]
        embed = discord.Embed(title="家の上空の飛行機", color=0xBEBEFE)
        embed.add_field(name="受信中の機体", value=f"{len(aircraft)} 機（位置あり {len(with_pos)} 機）", inline=False)
        if with_pos:
            near = min(with_pos, key=lambda a: float(a["r_dst"]))
            d = adsb.describe(near)
            embed.add_field(
                name="いちばん近い機体",
                value=f"{d['登録記号']} {d['機種']}\n{d['運航者']}\n{d['高度']}・{d['家からの距離・方角']}",
                inline=False,
            )
        military = [det for det in adsb.detect(aircraft, self.gov_pattern) if det.kind == adsb.MILITARY]
        if military:
            embed.add_field(
                name="軍用機・政府機",
                value="\n".join(f"{det.aircraft.get('r') or det.hex} {det.aircraft.get('desc') or ''}" for det in military),
                inline=False,
            )
        if self.receiver_ok is False:
            embed.set_footer(text="受信機に接続できていません。表示は最後に取得できたときのものです。")
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Adsb(bot))
