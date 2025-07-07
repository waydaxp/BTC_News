#!/usr/bin/env python3
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from utils.generate_data import get_all_analysis

def flatten_ctx(ctx: dict) -> dict:
    """
    将 ctx 中的多周期数据扁平化，生成形如：
      btc_price_15m, btc_strategy_4h, eth_tp_1h, ...
    以及其他全局变量。
    """
    flat = {}

    # 周期列表
    tfs = ["15m", "1h", "4h"]

    # 对每个币种、每个周期扁平化
    for symbol in ("btc", "eth"):
        for tf in tfs:
            tf_data = ctx.get(symbol, {}).get(tf, {})
            for key, val in tf_data.items():
                flat[f"{symbol}_{key}_{tf}"] = val

    # 恐惧贪婪等全局变量
    flat["fg_idx"] = ctx.get("fg_idx", "-")
    flat["fg_txt"] = ctx.get("fg_txt", "-")
    flat["fg_emoji"] = ctx.get("fg_emoji", "")
    flat["page_update"] = ctx.get("page_update",
                                  datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

    return flat

def main():
    # 1. 获取原始分析数据
    ctx = get_all_analysis()

    # 2. 扁平化
    data = flatten_ctx(ctx)

    # 3. Jinja2 环境 & 渲染
    here = os.path.dirname(os.path.abspath(__file__))
    env = Environment(
        loader=FileSystemLoader(here),
        autoescape=True
    )
    template = env.get_template("index_template.html")
    html = template.render(data=data)

    # 4. 输出到 /var/www/html/index.html
    out_path = "/var/www/html/index.html"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ index.html 已生成并部署到 /var/www/html")

if __name__ == "__main__":
    main()
