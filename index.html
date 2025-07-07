#!/usr/bin/env python3
# generate_html.py

import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from utils.generate_data import get_all_analysis

def flatten_ctx(ctx: dict) -> dict:
    """
    把 btc/eth 的三周期数据扁平化为模板可以直接访问的字段：
      btc_price_15m, btc_strategy_4h, eth_tp_1h, ...
    并加上 fg_idx, fg_txt, fg_emoji, page_update.
    """
    flat = {}
    tfs = ["15m", "1h", "4h"]

    for symbol in ("btc", "eth"):
        symbol_data = ctx.get(symbol, {})
        for tf in tfs:
            tf_data = symbol_data.get(tf, {})
            for key, val in tf_data.items():
                flat[f"{symbol}_{key}_{tf}"] = val

    # 恐惧贪婪等全局字段
    flat["fg_idx"] = ctx.get("fg_idx", "-")
    flat["fg_txt"] = ctx.get("fg_txt", "-")
    flat["fg_emoji"] = ctx.get("fg_emoji", "")
    flat["page_update"] = ctx.get(
        "page_update",
        datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    )

    return flat

def main():
    # 1. 取得原始分析上下文
    ctx = get_all_analysis()
    # 2. 扁平化
    data = flatten_ctx(ctx)
    # 3. 渲染模板
    here = os.path.dirname(os.path.abspath(__file__))
    env = Environment(
        loader=FileSystemLoader(here),
        autoescape=True
    )
    tmpl = env.get_template("index_template.html")
    html = tmpl.render(data=data)
    # 4. 写出到静态目录
    out = "/var/www/html/index.html"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ index.html 已更新")

if __name__ == "__main__":
    main()
