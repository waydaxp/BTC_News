# utils/fetch_macro_events.py
"""
按日期升序返回未来宏观事件（最多 limit 条）。
事件列表可根据需要改为接口爬虫或手动维护 YAML。
"""

from __future__ import annotations
from datetime import datetime
from typing import List

# ---- 临时硬编码示例 ----
_RAW_EVENTS = [
    # name, date(YYYY-MM-DD), impact
    ("美国CPI公布",       "2025-06-28", "若超预期，BTC 或承压"),
    ("FOMC 利率决议",     "2025-07-03", "加息可能引发波动"),
    ("SEC 审查比特币 ETF", "2025-07-10", "若通过，或引发大涨"),
]

def get_macro_events(limit: int | None = None) -> List[str]:
    """
    返回 **未 HTML 转义** 的字符串列表，可直接 `<br>` 连接：

    [
        "- 美国CPI公布（2025-06-28，2 天后）：若超预期，BTC 或承压",
        "- FOMC 利率决议（2025-07-03，7 天后）：加息可能引发波动",
        ...
    ]
    """
    today = datetime.utcnow().date()

    rows = []
    for name, date_str, impact in _RAW_EVENTS:
        dt = datetime.strptime(date_str, "%Y-%m-%d").date()
        if dt < today:
            continue                          # 已过去的事件跳过
        d_left = (dt - today).days
        rows.append(f"- {name}（{date_str}，{d_left} 天后）：{impact}")

    rows.sort()                               # 升序
    return rows[:limit] if limit else rows
