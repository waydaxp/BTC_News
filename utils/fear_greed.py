"""
抓取 Crypto Fear & Greed Index
https://api.alternative.me/fng/
"""

from datetime import datetime
import requests


API = "https://api.alternative.me/fng/?limit=1&format=json"


def get_fear_and_greed():
    """
    返回 4 元组:
        idx   → int   指数 0-100
        text  → str   英文描述，如 "Greed"
        emoji → str   😨 / 😊 / 😐  (自定义)
        ts    → str   更新时间，UTC → Asia/Shanghai
    """
    r = requests.get(API, timeout=6).json()
    d = r["data"][0]

    idx = int(d["value"])
    text = d["value_classification"]   # Extreme Fear / Greed …

    # 简单映射到 emoji
    if idx >= 75:
        emoji = "🤩"
    elif idx >= 55:
        emoji = "😊"
    elif idx >= 45:
        emoji = "😐"
    elif idx >= 25:
        emoji = "😟"
    else:
        emoji = "😨"

    ts_utc = datetime.utcfromtimestamp(int(d["timestamp"]))
    ts = ts_utc.astimezone().strftime("%Y-%m-%d %H:%M")

    return idx, text, emoji, ts   # ← 只返回 4 个
