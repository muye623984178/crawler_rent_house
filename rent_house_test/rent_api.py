from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# 连接数据库
db = pymysql.connect(host='localhost', user='root', password='root', db='rent_house')
cursor = db.cursor()


# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')
#
#     # 在数据库中查找用户信息
#     sql = "SELECT * FROM users WHERE username=%s AND password=%s"
#     cursor.execute(sql, (username, password))
#     user = cursor.fetchone()
#
#     if user:
#         return jsonify({'status': 'success', 'message': '登录成功'})
#     else:
#         return jsonify({'status': 'fail', 'message': '用户名或密码错误'})


@app.route('/getData', methods=['GET'])
def getData():
    sql = "SELECT name, place, price, href, tag, square FROM ziru1"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        items_dict = [{'name': item[0], 'place': item[1], 'price': item[2], 'href': item[3], 'tag': item[4], 'square': item[5]} for item in result]
        return jsonify(items_dict)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)