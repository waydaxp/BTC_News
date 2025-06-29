# utils/fear_greed.py
"""
获取 Crypto Fear & Greed Index（恐惧与贪婪指数）
------------------------------------------------
返回元组：
    (idx: int, text: str, emoji: str, ts_bj: str)

示例：
    >>> from utils.fear_greed import get_fear_and_greed
    >>> get_fear_and_greed()
    (68, 'Greed', '😄', '2025-06-30 09:45')
"""

from __future__ import annotations

import datetime as _dt
import json
import requests
from zoneinfo import ZoneInfo

__all__ = ["get_fear_and_greed"]

_API = "https://api.alternative.me/fng/?limit=1&format=json"
_TZ_BJ = ZoneInfo("Asia/Shanghai")
_TZ_UTC = ZoneInfo("UTC")

_EMOJI_MAP = {
    "Extreme Fear": "😨",
    "Fear":         "😟",
    "Neutral":      "😐",
    "Greed":        "😊",
    "Extreme Greed":"😄",
}


def _query_api() -> dict:
    """向 API 发起网络请求并返回第一条记录（dict）。"""
    resp = requests.get(_API, timeout=8)
    resp.raise_for_status()
    obj: dict = json.loads(resp.text)
    if obj.get("data"):
        return obj["data"][0]
    raise RuntimeError("Invalid response from Fear & Greed API")


def _utc_to_bj(ts: int) -> str:
    """时间戳 → 北京时间字符串（YYYY-MM-DD HH:MM）"""
    return (
        _dt.datetime.fromtimestamp(ts, _TZ_UTC)
        .astimezone(_TZ_BJ)
        .strftime("%Y-%m-%d %H:%M")
    )


def get_fear_and_greed() -> tuple[int, str, str, str]:
    """
    Returns
    -------
    idx : int
        指数数值 0-100
    text : str
        文本描述（Extreme Fear/Fear/Neutral/…）
    emoji : str
        对应表情
    ts_bj : str
        北京时间字符串
    """
    d = _query_api()

    idx  = int(d["value"])
    text = d["value_classification"]
    ts_bj = _utc_to_bj(int(d["timestamp"]))
    emoji = _EMOJI_MAP.get(text, "🤔")

    return idx, text, emoji, ts_bj


# 快速自测
if __name__ == "__main__":
    print(get_fear_and_greed())
