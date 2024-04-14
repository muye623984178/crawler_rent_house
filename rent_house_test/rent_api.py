import requests
from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# 小程序的 appid 和 appsecret
APPID = 'wxe7134cbc391a01e4'
SECRET = 'e8973b95c8d3d4674c64e2d9dc1189e9'


@app.route('/login', methods=['POST'])
def login():
    code = request.json.get('code')
    if not code:
        return jsonify({'error': 'Missing code'}), 400

        # 调用微信服务器的 sns/jscode2session 接口
    url = f'https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={code}&grant_type=authorization_code'
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        # 打印出微信服务器的响应状态码和响应内容
        print(f"微信服务器返回状态码: {response.status_code}, 响应内容: {data}")
        return jsonify({'error': 'Failed to get response from WeChat server'}), 500

        # 检查请求是否成功
    if 'openid' in data and 'session_key' in data:
        # 在这里你可以将 openid 和 session_key 保存到数据库，或者返回给前端
        # 例如，返回 openid 给前端
        return jsonify({'openid': data['openid']})
    else:
        # 处理错误情况
        print(data)
        return jsonify({'error': 'Failed to get openid and session_key'}), 500


# 连接数据库
db = pymysql.connect(host='localhost', user='root', password='root', db='rent_house')
cursor = db.cursor()


@app.route('/getData', methods=['GET'])
def getData():
    sql = "SELECT name, place, price, href, tag, square, img_src ,source FROM house_info"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        items_dict = [
            {'name': item[0], 'place': item[1], 'price': item[2], 'href': item[3], 'tag': item[4], 'square': item[5],
             'img_src': item[6], 'source': item[7]} for item in result]
        return jsonify(items_dict)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
