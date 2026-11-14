import discord
from discord.member import Member,VoiceState
from discord.ext import commands
from discord.ext.commands import Context
import util.voice_state_update as voice_state_update
import util.fortune as fortune

class Notification(commands.Cog, name="notification"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member:Member, before:VoiceState, after:VoiceState):
        """
        ボイスチャンネル関連でユーザステータスが変更された場合に発火する関数
        """
        action = voice_state_update.Action.checkAction(member, after, before)
        match action:
            case voice_state_update.Action.CHANNEL_JOIN:
                if voice_state_update.isIntervalTimePassed(member, 10):
                    msg = f'「{member.name}」さんが <#{after.channel.id}> に参加しました。(今回のおみくじ：**{fortune.trans_jp(fortune.Omikuji.draw())}**)'
                    channel_name = self.bot.config["notice_voice_channel"]
                    channel = discord.utils.get(member.guild.text_channels, name=channel_name)
                    if channel is None:
                        self.bot.logger.warning(f"[notification] 通知先チャンネル「{channel_name}」が {member.guild.name} に見つかりません。")
                        return
                    await channel.send(msg)
            case voice_state_update.Action.CHANNEL_EXIT:
                pass
            case voice_state_update.Action.CHANNEL_MOVE:
                pass
            case _:
                pass
        return

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Notification(bot))
