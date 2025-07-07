import os
import datetime
from jinja2 import Environment, FileSystemLoader
from utils.generate_data import get_all_analysis

def flatten_ctx(ctx):
    """
    将多周期嵌套的 ctx 扁平化为 Jinja2 可用的上下文
    如 btc['15m']['price'] → btc_price_15m
    """
    flat = {}

    for symbol in ['btc', 'eth']:
        for tf in ['15m', '1h', '4h']:
            data = ctx.get(symbol, {}).get(tf, {})
            prefix = f"{symbol}_{tf}"
            for key, value in data.items():
                flat[f"{symbol}_{key}_{tf}"] = value

    # 添加额外信息，如 funding, fg_idx 等
    flat['btc_funding'] = ctx.get('btc', {}).get('funding', '-')
    flat['eth_funding'] = ctx.get('eth', {}).get('funding', '-')
    flat['fg_idx'] = ctx.get('fg_idx', '-')
    flat['fg_txt'] = ctx.get('fg_txt', '-')
    flat['fg_emoji'] = ctx.get('fg_emoji', '')
    flat['page_update'] = ctx.get('page_update', datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

    return flat

def main():
    ctx = get_all_analysis()
    flat_ctx = flatten_ctx(ctx)

    env = Environment(loader=FileSystemLoader('.'), autoescape=True)
    template = env.get_template("index_template.html")

    html = template.render(**flat_ctx)

    output_path = "/var/www/html/index.html"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ index.html 已生成并部署到 /var/www/html")

if __name__ == "__main__":
    main()
