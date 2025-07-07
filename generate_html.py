from generate_data import get_all_analysis
from jinja2 import Environment, FileSystemLoader
from jinja2.utils import concat
from jinja2.runtime import Undefined
import jinja2
import os

# 注册 attribute 函数
def jinja2_attribute(obj, name):
    if isinstance(obj, dict):
        return obj.get(name, "-")
    return getattr(obj, name, "-")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = base_dir

    env = Environment(
        loader=FileSystemLoader(template_dir),
        auto_reload=True
    )

    # 注册 attribute 过滤器为全局函数
    env.globals['attribute'] = jinja2_attribute

    ctx = get_all_analysis()
    ctx["predict_entry_comment"] = (
        "📌 建仓价为建议入场价，基于未来3根K线的平均低点及回测策略生成，"
        "旨在提高胜率并规避假突破风险。"
    )

    # 示例风险统计（如需动态计算，请替换）
    ctx["risk_stats"] = {
        "total_trades": 100,
        "tp_hits": 38,
        "sl_hits": 34,
        "neutral": 28,
        "tp_rate": "38.0%",
        "sl_rate": "34.0%",
        "neutral_rate": "28.0%"
    }

    # 扁平化 ctx（便于模板渲染）
    flat_ctx = {}
    for key, val in ctx.items():
        if isinstance(val, dict):
            for subkey, subval in val.items():
                flat_ctx[f"{key}_{subkey}"] = subval
        else:
            flat_ctx[key] = val

    # 将 flat_ctx 注册为模板全局变量 "_context"
    env.globals.update(_context=flat_ctx)

    # 渲染 HTML
    template = env.get_template("index_template.html")
    html = template.render(**flat_ctx)

    # 输出路径
    output_path = "/var/www/html/index.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ index.html 已生成并部署到 /var/www/html")

if __name__ == "__main__":
    main()
