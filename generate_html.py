"""
generate_html.py
----------------
读取 index_template.html → 替换占位符 → 根据方向保留做多/做空区块 → 生成 index.html
"""

from generate_data import get_all_analysis

# 1. 拉取数据
analysis = get_all_analysis()

# 2. 读取模板
with open("index_template.html", encoding="utf-8") as f:
    tpl = f.read()

# 3. 先执行一次 format()，填充常规占位符
#    同时把 4 个区块标记自身作为字符串传进去，防止 KeyError
html = tpl.format(
    # === BTC 指标 ===
    btc_price=analysis["btc_price"],
    btc_ma20=analysis["btc_ma20"],
    btc_rsi=analysis["btc_rsi"],
    btc_signal=analysis["btc_signal"],

    # === 选定方向参数 ===
    entry=analysis["entry"],
    stop=analysis["stop"],
    target=analysis["target"],
    risk=analysis["risk"],
    position=analysis["position"],
    strategy=analysis["strategy"].replace("\n", "<br>"),

    # === ETH ===
    eth_price=analysis["eth_price"],
    eth_ma20=analysis["eth_ma20"],
    eth_rsi=analysis["eth_rsi"],
    eth_signal=analysis["eth_signal"],

    # === 宏观 & 情绪 ===
    macro_events=analysis["macro_events"],
    fear_index=analysis["fear_index"],
    fear_level=analysis["fear_level"],
    fear_date=analysis["fear_date"],

    updated_time=analysis["updated_time"],

    # --- 区块标记自身占位，后续再替换 ---
    long_block_start="{long_block_start}",
    long_block_end="{long_block_end}",
    short_block_start="{short_block_start}",
    short_block_end="{short_block_end}",
)

# 4. 根据方向打开/注释对应区块
direction = analysis["direction"]           # long / short / neutral

if direction == "long":
    html = html.replace("{long_block_start}", "").replace("{long_block_end}", "")
    html = html.replace("{short_block_start}", "<!--").replace("{short_block_end}", "-->")
elif direction == "short":
    html = html.replace("{short_block_start}", "").replace("{short_block_end}", "")
    html = html.replace("{long_block_start}", "<!--").replace("{long_block_end}", "-->")
else:                                       # neutral
    html = html.replace("{long_block_start}", "<!--").replace("{long_block_end}", "-->")
    html = html.replace("{short_block_start}", "<!--").replace("{short_block_end}", "-->")

# 5. 写入输出文件
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ index.html 已生成 / 更新完毕")
