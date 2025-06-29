# utils/fetch_macro_events.py
"""
返回未来的宏观事件（示例数据，可替换为实时 API）。
调用：
    from utils.fetch_macro_events import get_macro_events
    rows = get_macro_events(limit=5)   # 返回列表[str]
"""

from datetime import datetime, date
from typing import List, Dict

# ---- ① 这里用静态示例；实际生产可以在这里调用金十 / TradingEconomics 等 API ----
_RAW_EVENTS: List[Dict[str, str]] = [
    {"name": "美国CPI公布",      "date": "2025-06-28", "impact": "若超预期，BTC 或承压"},
    {"name": "FOMC 利率决议",    "date": "2025-07-03", "impact": "加息可能引发波动"},
    {"name": "SEC 审查比特币 ETF", "date": "2025-07-10", "impact": "若通过，或引发大涨"},
    {"name": "非农就业数据",     "date": "2025-07-05", "impact": "就业强劲或加大加息预期"},
]

# -----------------------------------------------------------------------------
def get_macro_events(limit: int | None = None) -> list[str]:
    """
    返回未来宏观事件的字符串列表（已按日期排序）。
    
    Parameters
    ----------
    limit : int | None
        限制返回条数；None 表示返回全部。
    """
    today: date = datetime.utcnow().date()

    # 过滤掉已过去的
    future = [
        ev for ev in _RAW_EVENTS
        if datetime.strptime(ev["date"], "%Y-%m-%d").date() >= today
    ]

    # 按日期升序
    future.sort(key=lambda ev: ev["date"])

    if limit is not None:
        future = future[:limit]

    rows: list[str] = []
    for ev in future:
        ev_date = datetime.strptime(ev["date"], "%Y-%m-%d").date()
        left = (ev_date - today).days
        rows.append(f"- {ev['name']}（{ev['date']}，{left} 天后）：{ev['impact']}")

    return rows


# ---- 快速自测 --------------------------------------------------------------
if __name__ == "__main__":
    for line in get_macro_events(limit=5):
        print(line)
