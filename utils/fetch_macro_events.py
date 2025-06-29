# utils/fetch_macro_events.py

from datetime import datetime

def get_macro_event_summary():
    events = [
        {"name":"美国 CPI", "date":"2025-06-28", "impact":"超预期则 BTC 承压"},
        {"name":"FOMC 利率会议", "date":"2025-07-03", "impact":"或引发波动"},
        {"name":"SEC 比特币 ETF", "date":"2025-07-10", "impact":"若通过大涨"},
    ]

    today = datetime.now()
    lines = []
    for ev in events:
        d = datetime.strptime(ev["date"], "%Y-%m-%d")
        delta = (d - today).days
        lines.append(f"- {ev['name']}（{ev['date']}，{delta} 天后）：{ev['impact']}")
    return "\n".join(lines)
