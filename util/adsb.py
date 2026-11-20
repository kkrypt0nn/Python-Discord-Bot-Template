"""
ADS-B 受信機（readsb / tar1090）の aircraft.json から、通知したい機体を選ぶ処理。
discord に依存しないので、単体で試せる。

aircraft.json の項目は readsb の README-json.md を参照:
  hex（ICAO 24bit）、r（登録記号）、t（機種コード）、desc（機種名）、ownOp（運航者）、
  flight（便名）、alt_baro（気圧高度 ft、地上なら "ground"）、r_dst（受信機からの距離 nm）、
  r_dir（受信機から見た方角 度）、squawk、emergency、dbFlags（bit0=軍用）、seen（最後に受信してからの秒数）
"""
import re
from dataclasses import dataclass
from typing import Optional

MILITARY = "military"
EMERGENCY = "emergency"

# スコークの意味
EMERGENCY_SQUAWKS = {
    "7500": "7500（ハイジャック）",
    "7600": "7600（無線の故障）",
    "7700": "7700（緊急事態）",
}
# readsb の emergency 項目の意味（none 以外）
EMERGENCY_STATUS = {
    "general": "緊急事態",
    "lifeguard": "急患の搬送",
    "minfuel": "燃料が少ない",
    "nordo": "無線の故障",
    "unlawful": "不法な妨害（ハイジャック）",
    "downed": "墜落",
    "reserved": "予約値",
}

# 運航者の名前で政府・軍の機体を見分ける（readsb の軍用の目印が付いていない機体を拾うため）
DEFAULT_GOV_PATTERN = (
    r"GOVERNMENT|MINISTRY|SELF[- ]?DEFEN[CS]E|AIR FORCE|NAVY|ARMY|MARINE CORPS|COAST GUARD|"
    r"自衛隊|防衛省|海上保安庁|政府"
)

COMPASS = ["北", "北北東", "北東", "東北東", "東", "東南東", "南東", "南南東",
           "南", "南南西", "南西", "西南西", "西", "西北西", "北西", "北北西"]


@dataclass
class Detection:
    hex: str
    kind: str  # MILITARY か EMERGENCY
    reason: str  # 通知に書く理由
    aircraft: dict


def _emergency_reason(ac: dict) -> Optional[str]:
    squawk = str(ac.get("squawk") or "")
    if squawk in EMERGENCY_SQUAWKS:
        return "スコーク " + EMERGENCY_SQUAWKS[squawk]
    status = ac.get("emergency")
    if status and status != "none":
        return "緊急の状態: " + EMERGENCY_STATUS.get(status, status)
    return None


def _military_reason(ac: dict, gov_re: re.Pattern) -> Optional[str]:
    if int(ac.get("dbFlags") or 0) & 1:
        return "軍用機（機体データベースの目印）"
    op = ac.get("ownOp") or ""
    if op and gov_re.search(op):
        return "運航者が政府・軍"
    return None


def detect(aircraft: list, gov_pattern: str = DEFAULT_GOV_PATTERN, max_seen: float = 60) -> list:
    """aircraft.json の aircraft 配列から、通知の候補を返す（同じ機体でも種類ごとに1件）"""
    gov_re = re.compile(gov_pattern, re.IGNORECASE)
    found = []
    for ac in aircraft:
        hex_ = ac.get("hex")
        if not hex_ or float(ac.get("seen") or 0) > max_seen:
            continue
        reason = _military_reason(ac, gov_re)
        if reason:
            found.append(Detection(hex_, MILITARY, reason, ac))
        reason = _emergency_reason(ac)
        if reason:
            found.append(Detection(hex_, EMERGENCY, reason, ac))
    return found


def direction(deg) -> str:
    if deg is None:
        return "-"
    return COMPASS[int((float(deg) % 360) / 22.5 + 0.5) % 16]


def describe(ac: dict) -> dict:
    """通知に載せる項目を、日本語の表示用の文字列にする"""
    alt = ac.get("alt_baro")
    if alt == "ground":
        alt_s = "地上"
    elif isinstance(alt, (int, float)):
        alt_s = f"{alt:,} ft（約 {alt * 0.3048:,.0f} m）"
    else:
        alt_s = "不明"
    dst = ac.get("r_dst")
    if dst is not None:
        pos_s = f"{float(dst) * 1.852:.1f} km・{direction(ac.get('r_dir'))}"
    else:
        pos_s = "位置は受信できていません"
    model = " ".join(x for x in [ac.get("desc"), f"（{ac['t']}）" if ac.get("t") else None] if x)
    return {
        "登録記号": ac.get("r") or "-",
        "機種": model or "-",
        "運航者": ac.get("ownOp") or "-",
        "便名": (ac.get("flight") or "").strip() or "-",
        "高度": alt_s,
        "家からの距離・方角": pos_s,
        "スコーク": ac.get("squawk") or "-",
    }


class Notifier:
    """
    同じ機体を何度も通知しないための記録。(hex, kind) ごとに、最後に見かけた時刻を持つ。
    見かけている間は通知せず、renotify_sec 以上見かけなかった機体がまた来たときに通知する。
    """

    def __init__(self, renotify_sec: float) -> None:
        self.renotify_sec = renotify_sec
        self.last: dict = {}

    def should_notify(self, det: Detection, now: float) -> bool:
        key = (det.hex, det.kind)
        last = self.last.get(key)
        self.last[key] = now
        return last is None or now - last >= self.renotify_sec

    def forget_older_than(self, now: float) -> None:
        for key in [k for k, t in self.last.items() if now - t >= self.renotify_sec]:
            del self.last[key]
