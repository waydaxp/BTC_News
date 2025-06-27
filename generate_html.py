"""Render index.html from template with single‑direction suggestion."""
from generate_data import get_all_analysis
from datetime import datetime, timedelta

data = get_all_analysis()

# 读取模板
with open("index_template.html", "r", encoding="utf-8") as f:
    tpl = f.read()

# 先填充通用占位符
tpl_rendered = tpl.format(
    btc_price=data["btc_price"], btc_ma20=data["btc_ma20"], btc_rsi=data["btc_rsi"], btc_signal=data["btc_signal"],
    entry=data["entry"], stop=data["stop"], target=data["target"],
    risk=data["risk"], position=data["position"], strategy=data["strategy"],
    eth_price=data["eth_price"], eth_ma20=data["eth_ma20"], eth_rsi=data["eth_rsi"], eth_signal=data["eth_signal"],
    macro_events=data["macro_events"], fear_index=data["fear_index"], fear_level=data["fear_level"],
    fear_date=data["fear_date"], updated_time=data["updated_time"]
)

# === 条件块处理 ===
if data["direction"] == "long":
    # 保留做多块，注释做空块
    tpl_rendered = tpl_rendered.replace("{long_block_start}", "").replace("{long_block_end}", "")
    tpl_rendered = tpl_rendered.replace("{short_block_start}", "<!--").replace("{short_block_end}", "-->")
elif data["direction"] == "short":
    tpl_rendered = tpl_rendered.replace("{short_block_start}", "").replace("{short_block_end}", "")
    tpl_rendered = tpl_rendered.replace("{long_block_start}", "<!--").replace("{long_block_end}", "-->")
else:  # neutral
    tpl_rendered = tpl_rendered.replace("{long_block_start}", "<!--")\
                                 .replace("{long_block_end}", "-->")\
                                 .replace("{short_block_start}", "<!--")\
                                 .replace("{short_block_end}", "-->")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(tpl_rendered)

print("✅ index.html 已生成")
