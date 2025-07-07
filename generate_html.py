import os
import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from utils.generate_data import get_all_analysis

def flatten_ctx(ctx):
    """
    将多周期嵌套的 ctx 扁平化为 Jinja2 可用的上下文
    例如：ctx['btc']['15m']['price'] -> btc_price_15m
    """
    flat = {}

    for symbol in ['btc', 'eth']:
        for tf in ['15m', '1h', '4h']:
            data = ctx.get(symbol, {}).get(tf, {})
            for key, value in data.items():
                flat[f"{symbol}_{key}_{tf}"] = value

        # 每个 symbol 顶级数据（如 funding、4h entry/sl/tp 等）
        for key in ['funding', 'entry_4h', 'sl_4h', 'tp_4h', 'support_4h', 'resistance_4h', 'strategy_4h']:
            flat[f"{symbol}_{key}"] = ctx.get(symbol, {}).get(key, '-')

    # 全局信息
    flat['fg_idx'] = ctx.get('fg_idx', '-')
    flat['fg_txt'] = ctx.get('fg_txt', '-')
    flat['fg_emoji'] = ctx.get('fg_emoji', '')
    flat['page_update'] = ctx.get('page_update', datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

    return flat

def main():
    try:
        ctx = get_all_analysis()
        flat_ctx = flatten_ctx(ctx)

        env = Environment(
            loader=FileSystemLoader(searchpath='.'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template("index_template.html")

        html = template.render(**flat_ctx)

        output_path = "/var/www/html/index.html"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        print("✅ index.html 已生成并部署到 /var/www/html")

    except Exception as e:
        print("❌ 页面生成失败:", str(e))

if __name__ == "__main__":
    main()
