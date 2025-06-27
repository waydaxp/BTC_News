from generate_data import get_all_analysis
from jinja2 import Environment, FileSystemLoader
import os

def generate_html():
    # 获取所有分析数据
    data = get_all_analysis()

    # 调试：输出所有变量
    print("[DEBUG] HTML 渲染数据:", data)

    # 加载模板环境
    env = Environment(loader=FileSystemLoader(searchpath='.'))
    template = env.get_template("index_template.html")

    # 渲染模板
    rendered_html = template.render(data)

    # 保存为 index.html
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(rendered_html)
        print("[INFO] 成功生成 index.html")

if __name__ == "__main__":
    generate_html()
