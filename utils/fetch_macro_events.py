from datetime import datetime, timedelta
import requests

def get_macro_events(n_future: int = 5) -> list[str]:
    # 这里只用示例数据，若要实时抓取，请自行接入真实 API
    demo = [
        ("美国CPI",      "2025-06-28", "超预期→BTC承压"),
        ("FOMC利率会",   "2025-07-03", "加息或引波动"),
        ("SEC比特币ETF", "2025-07-10", "若通过大涨"),
    ]
    today = datetime.today()
    out = []
    for name, ds, imp in demo[:n_future]:
        d = datetime.strptime(ds, "%Y-%m-%d")
        days = (d - today).days
        out.append(f"- {name}（{ds}，{days}天后）：{imp}")
    return out
