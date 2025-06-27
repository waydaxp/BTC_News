# utils/fetch_macro.py
import datetime

def get_macro_events():
    today = datetime.date.today()
    events = [
        {"event": "美国CPI公布", "time": "2025-06-28", "impact": "若超预期，BTC或承压"},
        {"event": "FOMC利率会议", "time": "2025-07-03", "impact": "加息可能引发波动"},
        {"event": "SEC审查比特币ETF", "time": "2025-07-10", "impact": "若通过，或引发大涨"},
    ]
    message = "\n📅【宏观事件提醒】\n"
    for e in events:
        d = datetime.datetime.strptime(e["time"], "%Y-%m-%d").date()
        days = (d - today).days
        message += f"- {e['event']}（{e['time']}，{days}天后）：{e['impact']}\n"
    return message
