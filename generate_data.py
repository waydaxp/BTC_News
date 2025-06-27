from jinja2 import Environment, FileSystemLoader
from generate_data import get_all_analysis
from datetime import datetime

def generate_html():
    # 获取所有数据
    data = get_all_analysis()

    # 添加当前 UTC 更新时间（如需北京时间，可 + timedelta(hours=8)）
    data["last_updated"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # 加载模板文件
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("index_template.html")

    # 渲染 HTML 并写入文件
    rendered_html = template.render(data)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(rendered_html)

if __name__ == "__main__":
    generate_html()
