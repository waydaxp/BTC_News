from flask import Flask, render_template
from generate_data import get_all_analysis

app = Flask(__name__)

@app.route('/')
def index():
    ctx = get_all_analysis()
    return render_template('index_template.html', **ctx)

# 可选：保留调试用
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
