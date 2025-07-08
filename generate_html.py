#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
import pytz
from jinja2 import Environment, FileSystemLoader

# 确保以下导入路径与你项目结构一致
from utils.fetch_btc_data import get_btc_analysis
from utils.fetch_eth_data import get_eth_analysis
from utils.fetch_fear_greed import get_fear_and_greed

def main():
    # ─── 路径设置 ──────────────────────────
    BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_NAME = "index_template.html"
    TEMPLATE_PATH = os.path.join(BASE_DIR, TEMPLATE_NAME)
    OUTPUT_PATH   = os.path.join(BASE_DIR, "index.html")

    # ─── 抓取原始数据 ──────────────────────
    raw_btc = get_btc_analysis()   # e.g. {"15m": {...}, "1h": {...}, "4h": {...}}
    raw_eth = get_eth_analysis()
    fg      = get_fear_and_greed() # 可能返回 (value,text,emoji) 或者 {"value":..}

    # ─── 扁平化 data 字典 ────────────────
    data = {}

    # BTC 指标：btc_<字段>_<周期>
    for tf, metrics in (raw_btc or {}).items():
        for key, val in metrics.items():
            # 模板里用的是 data["btc_strategy_"~tf]
            field = "strategy" if key == "strategy_note" else key
            data[f"btc_{field}_{tf}"] = val

    # ETH 指标：eth_<字段>_<周期>
    for tf, metrics in (raw_eth or {}).items():
        for key, val in metrics.items():
            field = "strategy" if key == "strategy_note" else key
            data[f"eth_{field}_{tf}"] = val

    # 恐惧与贪婪：兼容 tuple 或 dict
    if isinstance(fg, tuple) and len(fg) >= 3:
        idx, txt, emoji = fg[0], fg[1], fg[2]
    else:
        idx   = fg.get("value")
        txt   = fg.get("text")
        emoji = fg.get("emoji")
    data["fg_idx"]   = idx
    data["fg_txt"]   = txt
    data["fg_emoji"] = emoji

    # 页面更新时间（北京时间）
    bj_tz    = pytz.timezone("Asia/Shanghai")
    now_str  = datetime.now(bj_tz).strftime("%Y-%m-%d %H:%M:%S")
    data["page_update"] = now_str

    # ─── （可选）调试：打印所有扁平化后的键值 ─────────
    # for k in sorted(data):
    #     print(f"{k} = {data[k]}")

    # ─── 渲染模板 ──────────────────────────
    try:
        env = Environment(
            loader=FileSystemLoader(BASE_DIR),
            autoescape=False
        )
        template = env.get_template(TEMPLATE_NAME)
    except Exception as e:
        print(f"[ERROR] 无法加载模板 {TEMPLATE_NAME}: {e}", file=sys.stderr)
        sys.exit(1)

    rendered = template.render(data=data)

    # ─── 写入 index.html ─────────────────────
    try:
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(rendered)
        print(f"✅ index.html 已更新：{now_str}")
    except Exception as e:
        print(f"[ERROR] 写入 {OUTPUT_PATH} 失败: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
