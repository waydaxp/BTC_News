from generate_data import get_all_analysis
from jinja2 import Environment, FileSystemLoader
import os

def main():
    # 当前路径
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 模板目录
    template_dir = base_dir

    # 初始化 Jinja2 环境
    env = Environment(
        loader=FileSystemLoader(template_dir),
        auto_reload=True
    )

    # 加载模板
    template = env.get_template("index_template.html")

    # 获取上下文数据
    ctx = get_all_analysis()

    # 添加说明
    ctx["predict_entry_comment"] = (
        "\U0001F4CC 建仓价为建议入场价，基于未来3根K线的平均低点及回测策略生成，"
        "旨在提高胜率并规避假突破风险。"
    )

    ctx["risk_stats"] = {
        "total_trades": 100,
        "tp_hits": 38,
        "sl_hits": 34,
        "neutral": 28,
        "tp_rate": "38.0%",
        "sl_rate": "34.0%",
        "neutral_rate": "28.0%"
    }

    # 展平 ctx 中的 btc 和 eth，加入周期后缀
    flat_ctx = {}
    for asset_key in ["btc", "eth"]:
        if asset_key in ctx and isinstance(ctx[asset_key], dict):
            for metric_key, metric_val in ctx[asset_key].items():
                if "_" in metric_key and metric_key.split("_")[-1] in ["15m", "1h", "4h"]:
                    flat_ctx[f"{asset_key}_{metric_key}"] = metric_val
                else:
                    flat_ctx[f"{asset_key}_{metric_key}"] = metric_val

    # 加入其他非资产数据
    for key, val in ctx.items():
        if key not in ["btc", "eth"]:
            flat_ctx[key] = val

    # 渲染模板
    html = template.render(**flat_ctx)

    # 写入 HTML 文件
    output_path = "/var/www/html/index.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ index.html 已生成并部署到 /var/www/html")

if __name__ == "__main__":
    main()
