# utils/fear_greed.py
"""
获取 Crypto Fear & Greed Index
数据源: https://api.alternative.me/fng/
文档:  https://alternative.me/crypto/fear-and-greed-index/
"""

from __future__ import annotations
import requests
from datetime import datetime, timezone
from typing import Tuple

_API = "https://api.alternative.me/fng/?limit=1&format=json"

def _call_api() -> dict | None:
    try:
        resp = requests.get(_API, timeout=3)
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError):
        return None


def get_fear_and_greed() -> Tuple[str, str]:
    """
    Returns
    -------
    id:  str   # 原始时间戳（秒）— 可当作唯一 id
    text: str  # '68 (Greed)' 这样的组合字符串
    """
    js = _call_api()
    if not js or "data" not in js:
        return "N/A", "N/A"

    item = js["data"][0]         # 最近一条
    score   = item["value"]      # '68'
    desc    = item["value_classification"].capitalize()  # 'Greed'
    ts_id   = item["timestamp"]  # '1722316800'

    return ts_id, f"{score} ({desc})"


# 快速本地测试
if __name__ == "__main__":
    print(get_fear_and_greed())
