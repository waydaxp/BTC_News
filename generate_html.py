from jinja2 import Environment, FileSystemLoader
from generate_data import get_all_analysis

def generate_html():
    # 获取数据（BTC, ETH, 宏观事件, 恐惧指数等）
    data = get_all_analysis()

    # 设置 Jinja2 模板环境，加载当前目录
    env = Environment(loader=FileSystemLoader('.'))

    # 加载模板文件（确保是 index_template.html）
    template = env.get_template('index_template.html')

    # 渲染模板
    rendered_html = template.render(data)

    # 输出为 index.html，供 GitHub Pages 展示
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(rendered_html)

if __name__ == "__main__":
    generate_html()
