# utils/fear_greed.py
"""
获取加密货币「恐惧与贪婪指数」
数据源：https://api.alternative.me/fng/
"""

from __future__ import annotations
from datetime import datetime, timezone
import requests, json, os, pathlib

_URL   = "https://api.alternative.me/fng/"
CACHE  = pathlib.Path(__file__).with_suffix(".cache.json")  # 本地缓存，防止接口抽风
TIMEOUT = 5


def _fetch_live() -> dict[str, str] | None:
    try:
        resp = requests.get(_URL, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()["data"][0]          # 取最新一条
        data["cache_ts"] = datetime.now(timezone.utc).isoformat()
        CACHE.write_text(json.dumps(data, ensure_ascii=False))
        return data
    except Exception:
        return None


def _load_cache(max_age_min: int = 60) -> dict[str, str] | None:
    """读取 ≤max_age_min 分钟的缓存，避免频繁请求"""
    if not CACHE.exists():
        return None
    try:
        data = json.loads(CACHE.read_text())
        ts   = datetime.fromisoformat(data["cache_ts"])
        age  = (datetime.now(timezone.utc) - ts).total_seconds() / 60
        return data if age <= max_age_min else None
    except Exception:
        return None


def get_fear_and_greed() -> str:
    """
    返回示例：
    >>> '46（Fear）'
    网络完全失败时 → 'N/A'
    """
    data = _fetch_live() or _load_cache()     # 先尝试实时，再回退缓存
    if not data:
        return "N/A"

    value  = data["value"]
    label  = data["value_classification"]     # Extreme Fear / Greed / Neutral
    return f"{value}（{label}）"
