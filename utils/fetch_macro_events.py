# utils/fetch_macro_events.py
"""
拉取 CoinMarketCal 未来 7 天内与 BTC / ETH 相关的高重要度事件
需在 GitHub Secrets 中设置 COINMARKETCAL_KEY
"""

import os, requests, datetime as dt
from typing import List

_API = "https://developers.coinmarketcal.com/v1/events"
_HEADERS = {"x-api-key": os.getenv("COINMARKETCAL_KEY")}

def _call_api() -> list[dict]:
    params = {
        "symbols": "BTC,ETH",
        "page": 1,
        "max": 10,
        "dateRangeStart": dt.date.today().isoformat(),
        "dateRangeEnd":   (dt.date.today() + dt.timedelta(days=7)).isoformat(),
        "sortBy": "hot",      # 热度/重要度
    }
    try:
        r = requests.get(_API, params=params, headers=_HEADERS, timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.RequestException:
        return []

def get_macro_event_summary() -> str:
    events = _call_api()
    if not events:
        return "⚠️ 无法获取实时宏观事件，请稍后再试。"

    lines: List[str] = []
    today = dt.date.today()
    for ev in events:
        ev_date = dt.datetime.fromisoformat(ev["date"])
        days = (ev_date.date() - today).days
        lines.append(
            f"- {ev['title']}（{ev_date:%m-%d}，{days} 天后）：{ev['description'][:40]}..."
        )
    return "\n".join(lines)
