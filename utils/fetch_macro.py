# utils/fetch_macro.py
from datetime import date, datetime

def get_macro_events():
    today = date.today()
    events = [
        {"event": "美国CPI公布", "time": "2025-06-28", "impact": "若超预期，BTC或承压"},
        {"event": "FOMC利率会议", "time": "2025-07-03", "impact": "加息可能引发波动"},
        {"event": "SEC审查比特币ETF", "time": "2025-07-10", "impact": "若通过，或引发大涨"},
    ]
    msg = "\n📅【宏观事件提醒】"
    for e in events:
        d = datetime.strptime(e["time"], "%Y-%m-%d").date()
        left = (d - today).days
        msg += f"\n- {e['event']}（{e['time']}，{left}天后）：{e['impact']}"
    return msg


# utils/fetch_sentiment.py
import requests
