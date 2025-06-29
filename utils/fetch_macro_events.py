"""
utils.fetch_macro_events
------------------------
返回未来的宏观事件列表。

★ 保证函数签名: get_macro_events(limit: int | None = None) → list[str]
★ generate_data.py 会调用:
    "<br>".join(get_macro_events(limit=5))
"""

from datetime import datetime, date
from typing import List, Dict

# ------------------------------------------------------------
# ❶ 示例静态数据 —— 实际可替换为实时 API 抓取
_RAW_EVENTS: List[Dict[str, str]] = [
    {"name": "美国 CPI 公布",     "date": "2025-06-28", "impact": "若超预期，BTC 或承压"},
    {"name": "FOMC 利率决议",     "date": "2025-07-03", "impact": "加息可能引发波动"},
    {"name": "SEC 审查比特币 ETF", "date": "2025-07-10", "impact": "若通过，或引发大涨"},
    {"name": "非农就业报告",      "date": "2025-07-05", "impact": "就业强劲或加大加息预期"},
]

# ------------------------------------------------------------
def get_macro_events(limit: int | None = None) -> list[str]:
    """
    返回按日期升序的未来事件描述列表。
    
    Parameters
    ----------
    limit : int | None
        返回的条目数上限；None = 全部。
    """
    today: date = datetime.utcnow().date()

    # 过滤未来事件
    upcoming = [
        ev for ev in _RAW_EVENTS
        if datetime.strptime(ev["date"], "%Y-%m-%d").date() >= today
    ]

    # 按日期排序
    upcoming.sort(key=lambda ev: ev["date"])

    if limit is not None:
        upcoming = upcoming[:limit]

    rows: list[str] = []
    for ev in upcoming:
        ev_date = datetime.strptime(ev["date"], "%Y-%m-%d").date()
        dleft   = (ev_date - today).days
        rows.append(f"- {ev['name']}（{ev['date']}，{dleft} 天后）：{ev['impact']}")

    return rows


# ------------------------------------------------------------
# 快速自测：直接运行文件打印效果
if __name__ == "__main__":
    print("\n".join(get_macro_events(limit=5)))
