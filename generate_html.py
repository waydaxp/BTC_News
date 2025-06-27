"""
Read index_template.html, replace placeholders,
conditionally keep long/short block according to direction,
then write index.html
"""

from generate_data import get_all_analysis

analysis = get_all_analysis()

with open("index_template.html", encoding="utf-8") as f:
    tpl = f.read()

# --- 普通占位符替换 ---
html = tpl.format(
    btc_price=analysis["btc_price"],
    btc_ma20=analysis["btc_ma20"],
    btc_rsi=analysis["btc_rsi"],
    btc_signal=analysis["btc_signal"],

    entry=analysis["entry"],
    stop=analysis["stop"],
    target=analysis["target"],
    risk=analysis["risk"],
    position=analysis["position"],
    strategy=analysis["strategy"].replace("\n", "<br>"),

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

# --- 条件块处理 ---
if analysis["direction"] == "long":
    html = html.replace("{long_block_start}", "").replace("{long_block_end}", "")
    html = html.replace("{short_block_start}", "<!--").replace("{short_block_end}", "-->")
elif analysis["direction"] == "short":
    html = html.replace("{short_block_start}", "").replace("{short_block_end}", "")
    html = html.replace("{long_block_start}", "<!--").replace("{long_block_end}", "-->")
else:  # neutral
    html = html.replace("{long_block_start}", "<!--").replace("{long_block_end}", "-->")
    html = html.replace("{short_block_start}", "<!--").replace("{short_block_end}", "-->")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ index.html 已生成")
