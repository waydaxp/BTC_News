import os
from jinja2 import Environment, FileSystemLoader
from utils.generate_data import get_all_analysis

def flatten_ctx(ctx: dict) -> dict:
    """
    将嵌套的多周期 ctx 展平为扁平 key，例如 btc_price_4h 等
    """
    flat = {}
    for coin in ["btc", "eth"]:
        data = ctx.get(coin, {})
        for tf in ["15m", "1h", "4h"]:
            for k in ["price", "ma20", "rsi", "atr", "volume", "support", "resistance", "signal", "tp", "sl", "win_rate", "strategy"]:
                val = data.get(f"{k}_{tf}", "-")
                flat[f"{coin}_{k}_{tf}"] = val
        flat[f"{coin}_funding"] = data.get("funding", "-")

    # 直接加入原始字段
    flat.update({
        "fg_idx": ctx.get("fg_idx", "-"),
        "fg_txt": ctx.get("fg_txt", "-"),
        "fg_emoji": ctx.get("fg_emoji", "-"),
        "fg_ts": ctx.get("fg_ts", "-"),
        "macro_events": ctx.get("macro_events", "暂无数据"),
        "page_update": ctx.get("page_update", "")
    })
    return flat

def main():
    try:
        ctx = get_all_analysis()
        flat_ctx = flatten_ctx(ctx)

        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template("index_template.html")
        html = template.render(**flat_ctx)

        output_path = "/var/www/html/index.html"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"✅ 页面已生成: {output_path}")
    except Exception as e:
        print(f"❌ 页面生成失败: {e}")

if __name__ == "__main__":
    main()
