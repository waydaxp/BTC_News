from generate_data import get_all_analysis
from jinja2 import Environment, FileSystemLoader

# 定义 attribute()，允许模板中动态访问变量
def attribute(obj, name):
    return obj.get(name, "")

def main():
    # 获取上下文
    ctx = get_all_analysis()

    # 构建模板环境，并注册 attribute 函数
    env = Environment(
        loader=FileSystemLoader("."),  # 模板所在目录
        autoescape=True
    )
    env.globals['attribute'] = attribute  # ✅ 注册给模板使用

    # 加载模板并渲染
    template = env.get_template("index_template.html")
    html = template.render(**ctx)

    # 保存 HTML
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ index.html 已更新")

if __name__ == "__main__":
    main()
