from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/ziru', methods=['POST'])
def your_function():
    # 从请求中获取数据
    data = request.json

    # 在这里处理你的业务逻辑
    result = process_data(data)

    # 返回响应
    return jsonify(result)


def process_data(data):
    # 你的数据处理逻辑
    return processed_data


if __name__ == '__main__':
    app.run(debug=True)