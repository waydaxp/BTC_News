from generate_data import get_all_analysis
from jinja2 import Environment, FileSystemLoader
import os

def main():
    # 获取当前目录
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 设置模板目录
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

    # ✅ 添加建仓说明
    ctx["predict_entry_comment"] = (
        "📌 建仓价为建议入场点位，结合未来价格均值和回测统计生成，用于提高胜率并规避假突破。"
    )

    # ✅ 添加策略回测统计示例
    ctx["risk_stats"] = {
        "total_trades": 100,
        "tp_hits": 38,
        "sl_hits": 34,
        "neutral": 28,
        "tp_rate": "38.0%",
        "sl_rate": "34.0%",
        "neutral_rate": "28.0%"
    }

    # ✅ 扁平化 ctx，用于模板中直接使用
    flat_ctx = {}
    for key, val in ctx.items():
        if isinstance(val, dict):
            for subkey, subval in val.items():
                flat_ctx[f"{key}_{subkey}"] = subval
        else:
            flat_ctx[key] = val

    # ✅ 渲染 HTML 内容
    html = template.render(**flat_ctx)

    # ✅ 写入到 Web 根目录
    output_path = "/var/www/html/index.html"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # 保证目录存在
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ index.html 已生成并部署到 /var/www/html")

if __name__ == "__main__":
    main()
