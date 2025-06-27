# generate_html.py

from generate_data import get_all_analysis
from datetime import datetime, timedelta

# 获取数据
analysis = get_all_analysis()

# 获取当前北京时间
now_utc = datetime.utcnow() + timedelta(hours=8)
timestamp_str = now_utc.strftime("%Y-%m-%d %H:%M")

# 读取 HTML 模板
with open("index_template.html", "r", encoding="utf-8") as f:
    template = f.read()

# 渲染 HTML
output = template.format(
    btc_price=analysis["btc_price"],
    btc_ma20=analysis["btc_ma20"],
    btc_rsi=analysis["btc_rsi"],
    btc_signal=analysis["btc_signal"],

    btc_long_entry=analysis["btc_long_entry"],
    btc_long_stop=analysis["btc_long_stop"],
    btc_long_target=analysis["btc_long_target"],
    btc_long_risk=analysis["btc_long_risk"],
    btc_long_position=analysis["btc_long_position"],
    btc_long_strategy=analysis["btc_long_strategy"],

    btc_short_entry=analysis["btc_short_entry"],
    btc_short_stop=analysis["btc_short_stop"],
    btc_short_target=analysis["btc_short_target"],
    btc_short_risk=analysis["btc_short_risk"],
    btc_short_position=analysis["btc_short_position"],
    btc_short_strategy=analysis["btc_short_strategy"],

    eth_price=analysis["eth_price"],
    eth_ma20=analysis["eth_ma20"],
    eth_rsi=analysis["eth_rsi"],
    eth_signal=analysis["eth_signal"],

    macro_events=analysis["macro_events"],
    fear_index=analysis["fear_index"],
    fear_level=analysis["fear_level"],
    fear_date=analysis["fear_date"],
    updated_time=analysis["updated_time"]
)

# 写入 index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(output)

print("✅ HTML 页面已更新成功")
