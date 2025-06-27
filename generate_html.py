# generate_html.py

import os
from jinja2 import Environment, FileSystemLoader
from generate_data import get_all_analysis

def generate_html():
    # 获取数据
    data = get_all_analysis()

    # 初始化 Jinja2 环境
    env = Environment(loader=FileSystemLoader(searchpath="."))
    template = env.get_template("index.html")

    # 渲染模板
    rendered_html = template.render(**data)

    # 输出最终 HTML
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(rendered_html)

    print("✅ HTML 页面已生成，并写入 index.html")

if __name__ == "__main__":
    generate_html()
