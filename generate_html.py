from generate_data import get_all_analysis
from jinja2 import Environment, FileSystemLoader

def main():
    # 获取数据上下文
    ctx = get_all_analysis()

    # 设置 Jinja2 模板环境
    env = Environment(
        loader=FileSystemLoader("."),  # 模板文件位于当前目录
        autoescape=True
    )

    # 加载模板文件
    template = env.get_template("index_template.html")

    # 渲染模板
    html = template.render(**ctx)

    # 写入输出 HTML 文件
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ index.html 已更新")

if __name__ == "__main__":
    main()
