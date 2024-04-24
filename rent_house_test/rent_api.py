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
    sql = "SELECT name, place, price, href, tag, square, img_src, source, id FROM house_info"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        if result is not None:
            items_dict = [
                {'name': item[0], 'place': item[1], 'price': item[2], 'href': item[3], 'tag': item[4],
                 'square': item[5],
                 'img_src': item[6], 'source': item[7], 'houseId': item[8]} for item in result]
            return jsonify(items_dict)
    except Exception as e:
        print(f"An error occurred in getData: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/getStoreData', methods=['POST'])
def getStoreData():
    openId = request.json.get('openid')
    # print(openId)
    if not openId:
        return jsonify({'error': 'Missing openId'}), 400
    sql = ('SELECT house_info.name, house_info.price, house_info.square, house_info.place, house_info.tag, '
           'house_info.href, house_info.img_src, house_info.source, house_info.id FROM house_info,store_info WHERE userId = %s AND '
           'house_info.`id` = store_info.`houseId`')
    try:
        cursor.execute(sql, openId)
        # db.commit()
        result = cursor.fetchall()
        if result is not None:
            items_dict = [
                {'name': item[0], 'place': item[3], 'price': item[1], 'href': item[5], 'tag': item[4],
                 'square': item[2],
                 'img_src': item[6], 'source': item[7], 'houseId': item[8]} for item in result]
            # print(items_dict)
            return jsonify(items_dict)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/deleteStore', methods=['POST'])
def deleteStore():
    openId = request.json.get('openid')
    houseId = request.json.get('houseId')
    print(openId)
    print(houseId)
    if not openId:
        return jsonify({'error': 'Missing openId'}), 400
    sql = 'DELETE FROM store_info WHERE userId = %s AND houseId = %s'
    try:
        cursor.execute(sql, (openId, houseId))
        db.commit()
        return 'success: delete'
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/insertStore', methods=['POST'])
def insertData():
    openId = request.json.get('openid')
    houseId = request.json.get('houseId')
    # print(openId)
    # print(houseId)
    if not openId:
        return jsonify({'error': 'Missing openId'}), 400
    sql = 'INSERT INTO store_info VALUES(%s, %s)'
    try:
        cursor.execute(sql, (openId, houseId))
        db.commit()
        return 'success: insert'
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/judgeStore', methods=['POST'])
def judgeStore():
    openId = request.json.get('openid')
    print(openId)
    if not openId:
        return jsonify({'error': 'Missing openId'}), 400
    sql = 'SELECT houseId FROM store_info WHERE userId=%s'
    try:
        cursor.execute(sql, openId)
        result = cursor.fetchall()
        if result is None:
            return "None"
        else:
            favoriteMap = {}
            for item in result:
                # print(item[0])
                favoriteMap[item[0]] = True
            print(favoriteMap)
            return jsonify(favoriteMap)

    except Exception as e:
        print(f"An error occurred in judgeStore: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
