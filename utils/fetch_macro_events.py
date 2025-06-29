# utils/fetch_macro_events.py
from datetime import datetime

_RAW_EVENTS = [
    # ……这里放你真正的事件抓取 / API 结果……
]

def get_macro_events(limit: int | None = None) -> list[str]:
    """
    返回未来宏观事件的字符串列表。
    参数
    ----
    limit : int | None
        限制返回条数；None 表示全部返回。
    """
    today = datetime.today().date()
    future = [e for e in _RAW_EVENTS
              if datetime.strptime(e["date"], "%Y-%m-%d").date() >= today]

    # 按日期排序
    future.sort(key=lambda x: x["date"])

    # 仅保留前 limit 条
    if limit is not None:
        future = future[:limit]

    # 组装为人类可读行
    rows = []
    for ev in future:
        d = datetime.strptime(ev["date"], "%Y-%m-%d").date()
        left = (d - today).days
        rows.append(f"- {ev['name']}（{ev['date']}，{left} 天后）：{ev['impact']}")
    return rows
