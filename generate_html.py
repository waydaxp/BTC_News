from generate_data import get_all_analysis
from datetime import datetime, timedelta

# 获取全部数据
analysis = get_all_analysis()

# 获取当前北京时间
now_utc = datetime.utcnow() + timedelta(hours=8)
timestamp_str = now_utc.strftime("%Y-%m-%d %H:%M")

# 读取 HTML 模板
with open("index_template.html", "r", encoding="utf-8") as f:
    template = f.read()

# 渲染内容
output = template.format(
    btc_price=analysis["btc_price"],
    btc_ma20=analysis["btc_ma20"],
    btc_rsi=analysis["btc_rsi"],
    btc_signal=analysis["btc_signal"],
    btc_entry=analysis["btc_entry"],
    btc_stop=analysis["btc_stop"],
    btc_target=analysis["btc_target"],
    btc_risk=analysis["btc_risk"],
    btc_position=analysis["btc_position"],

    btc_long_strategy=analysis.get("btc_long_strategy", ""),
    btc_short_strategy=analysis.get("btc_short_strategy", ""),

    eth_price=analysis["eth_price"],
    eth_ma20=analysis["eth_ma20"],
    eth_rsi=analysis["eth_rsi"],
    eth_signal=analysis["eth_signal"],

    macro_events=analysis["macro_events"],
    fear_index=analysis["fear_index"],
    fear_level=analysis["fear_level"],
    fear_date=analysis["fear_date"],
    updated_time=timestamp_str
)

# 输出为 index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(output)

print("✅ HTML 页面已更新")
