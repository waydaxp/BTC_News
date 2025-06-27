# utils/fetch_macro_events.py
from datetime import datetime

def get_macro_event_summary():
    today = datetime.today()
    
    events = [
        {
            "name": "美国CPI公布",
            "date": "2025-06-28",
            "impact": "若超预期，BTC或承压"
        },
        {
            "name": "FOMC利率会议",
            "date": "2025-07-03",
            "impact": "加息可能引发波动"
        },
        {
            "name": "SEC审查比特币ETF",
            "date": "2025-07-10",
            "impact": "若通过，或引发大涨"
        }
    ]

    result = []
    for event in events:
        event_date = datetime.strptime(event["date"], "%Y-%m-%d")
        delta_days = (event_date - today).days
        line = f"- {event['name']}（{event['date']}，{delta_days}天后）：{event['impact']}"
        result.append(line)

    return "\n".join(result)
