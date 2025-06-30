# generate_html.py

from generate_data import get_all_analysis
from jinja2 import Environment, FileSystemLoader
import os

def main():
    # 获取当前文件目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 设置模板文件目录
    template_dir = base_dir  # 若你将 index_template.html 放在 templates 目录，请改为 os.path.join(base_dir, "templates")

    # 加载模板
    env = Environment(loader=FileSystemLoader(template_dir), cache_size=0)
    template = env.get_template("index_template.html")

    # 获取所有分析数据
    ctx = get_all_analysis()

    # 渲染模板
    html = template.render(ctx=ctx, **ctx)

    # 写入输出文件
    output_path = os.path.join(base_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ index.html 已生成")

if __name__ == "__main__":
    main()
