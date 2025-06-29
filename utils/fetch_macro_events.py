# utils/fetch_macro_events.py
"""
返回未来 N 条重要宏观事件列表（已按时间升序）。
本例仍用静态示范数据，你可以替换为自己的爬虫或 API 调用。
"""
from datetime import datetime
from typing import List

# —— 示例静态事件 —— #
_RAW_EVENTS = [
    {"name": "美国CPI公布",      "date": "2025-06-28", "impact": "若超预期，BTC 或承压"},
    {"name": "FOMC 利率会议",   "date": "2025-07-03", "impact": "加息可能引发波动"},
    {"name": "SEC 审查比特币 ETF", "date": "2025-07-10", "impact": "若通过，或引发大涨"},
    {"name": "欧洲央行利率决议", "date": "2025-07-18", "impact": "欧元波动或外溢至加密"},
    {"name": "美国 PCE 物价指数", "date": "2025-07-26", "impact": "通胀高企或利空风险资产"},
]
# ———————————— #

def get_macro_events(n_future: int = 5) -> List[str]:
    """
    返回未来 n_future 条事件，格式已排好：
        “美国CPI公布（2025-06-28，2天后）：若超预期，BTC 或承压”
    """
    today = datetime.utcnow().date()

    events_sorted = sorted(_RAW_EVENTS, key=lambda e: e["date"])
    results = []

    for ev in events_sorted:
        if len(results) >= n_future:
            break

        ev_date = datetime.strptime(ev["date"], "%Y-%m-%d").date()
        delta   = (ev_date - today).days
        # 只保留今天及未来的事件
        if delta >= 0:
            line = f"{ev['name']}（{ev['date']}，{delta}天后）：{ev['impact']}"
            results.append(line)

    return results
