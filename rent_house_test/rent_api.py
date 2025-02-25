import logging
import os
from io import BytesIO

import requests
from flask import Flask, request, jsonify, make_response, send_file
import pymysql
from openpyxl import Workbook
import pandas as pd
from rent_house import ziru_crawl, lianJia_crawl, woAiWoJia_crawl, process

app = Flask(__name__)

# 小程序的 appid 和 appsecret
APPID = ''
SECRET = ''


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
excel_path = 'D:/muye/学业/爬虫系统/实现/rent_house_test/excel_file/ziRu.xlsx'


@app.route('/crawl', methods=['POST'])
def crawl():
    platform = request.json.get('platform')
    if platform == "ziRu":
        ziru_crawl()
    elif platform == "lianJia":
        lianJia_crawl()
    elif platform == "woAiWoJia":
        woAiWoJia_crawl()
    elif platform == "all":
        woAiWoJia_crawl()
        lianJia_crawl()
        ziru_crawl()
    else:
        return jsonify({'error': "platform参数错误"})
    return jsonify({'success': platform + "爬取完成"})


@app.route('/export', methods=['POST'])
def export():
    platform = request.json.get('platform')
    if platform == "ziRu":
        df = pd.read_sql_query("SELECT * FROM ziru1", db)
    elif platform == "lianJia":
        df = pd.read_sql_query("SELECT * FROM lianjia", db)
    elif platform == "woAiWoJia":
        df = pd.read_sql_query("SELECT * FROM woaiwojia", db)
    elif platform == "all":
        df = pd.read_sql_query("SELECT * FROM house_info", db)
    else:
        return jsonify({'error': "platform参数错误"})

    global excel_path
    excel_path = 'D:/muye/学业/爬虫系统/实现/rent_house_test/excel_file/' + platform + '.xlsx'
    df.to_excel(excel_path, index=False)
    # return send_file(excel_path, as_attachment=True)
    return jsonify({'download_url': 'http://127.0.0.1:5000/download'})


@app.route('/download', methods=['GET'])
def download_file():
    global excel_path
    print(excel_path)
    # 检查文件是否存在
    if os.path.exists(excel_path):
        # 发送文件
        return send_file(excel_path, as_attachment=True)
    else:
        # 文件路径不存在，返回错误响应
        return "文件路径不存在", 404


@app.route('/judgeIdentity', methods=['POST'])
def judgeIdentity():
    openId = request.json.get('openid')
    # openId = request.args.get('openid')
    # print(openId)
    if not openId:
        return jsonify({'error': 'Missing openId'}), 400
    sql = 'SELECT openId FROM admin WHERE openId=%s'
    try:
        cursor.execute(sql, openId)
        result = cursor.fetchall()
        if result is None:
            return jsonify({'flag': 'false'})
        else:
            return jsonify({'flag': 'true'})

    except Exception as e:
        print(f"An error occurred in judgeIdentity: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/processData', methods=['POST'])
def processData():
    process()
    return jsonify({'success': 'successfully processing data'})

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


@app.route('/getData_page', methods=['GET'])
def getData_page():
    page = request.args.get('page', 1, type=int)  # 默认第一页
    per_page = 20  # 每页显示20条数据
    offset = (page - 1) * per_page  # 计算偏移量

    try:
        # 执行SQL查询
        sql = ("SELECT name, place, price, href, tag, square, img_src, source, id FROM house_info "
               "LIMIT %s OFFSET %s")
        cursor.execute(sql, (per_page, offset))
        result = cursor.fetchall()
        if result is not None:
            items_dict = [
                {'name': item[0], 'place': item[1], 'price': item[2], 'href': item[3], 'tag': item[4],
                 'square': item[5],
                 'img_src': item[6], 'source': item[7], 'houseId': item[8]} for item in result]
            return jsonify(items_dict)
    except Exception as e:
        # 处理异常
        print(e)
        return jsonify({'error': 'Failed to retrieve data'}), 500


@app.route('/getDataByArea', methods=['POST'])
def getDataByArea():
    area = request.json.get('area')
    sql = "SELECT name, place, price, href, tag, square, img_src, source, id FROM house_info where area = %s"
    try:
        cursor.execute(sql, area)
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


@app.route('/getDataByArea_page', methods=['GET'])
def getDataByArea_page():
    page = request.args.get('page', 1, type=int)  # 默认第一页
    area = request.args.get('area', '北京', type=str)
    per_page = 20  # 每页显示20条数据
    offset = (page - 1) * per_page  # 计算偏移量

    try:
        # 执行SQL查询
        sql = ("SELECT name, place, price, href, tag, square, img_src, source, id, floor, scale, direction FROM house_info WHERE area=%s"
               "LIMIT %s OFFSET %s")
        cursor.execute(sql, (area, per_page, offset))
        result = cursor.fetchall()
        if result is not None:
            # print(result)
            items_dict = [
                {'name': item[0], 'place': item[1], 'price': item[2], 'href': item[3], 'tag': item[4],
                 'square': item[5],
                 'img_src': item[6], 'source': item[7], 'houseId': item[8], 'floor': item[9], 'scale': item[10], 'direction': item[11]} for item in result]
            return jsonify(items_dict)
    except Exception as e:
        # 处理异常
        print(e)
        return jsonify({'error': 'Failed to retrieve data'}), 500


@app.route('/findData', methods=['GET'])
def findData():
    word = request.args.get('word')
    area = request.args.get('area')
    word = '%' + word + '%'
    sql = "SELECT NAME, place, price, href, tag, square, img_src, source, id FROM house_info WHERE NAME LIKE %s OR place LIKE %s OR tag LIKE %s AND area = %s"
    try:
        cursor.execute(sql, (word, word, word,area))
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


@app.route('/getStoreData', methods=['GET'])
def getStoreData():
    # openId = request.json.get('openid')
    openId = request.args.get('openid')
    # print(openId)
    if not openId:
        return jsonify({'error': 'Missing openId'}), 400
    sql = ('SELECT house_info.name, house_info.price, house_info.square, house_info.place, house_info.tag, '
           'house_info.href, house_info.img_src, house_info.source, house_info.id, house_info.floor, house_info.scale, house_info.direction FROM house_info,store_info WHERE '
           'userId = %s AND '
           'house_info.`id` = store_info.`houseId`')
    try:
        cursor.execute(sql, openId)
        result = cursor.fetchall()
        if result is not None:
            items_dict = [
                {'name': item[0], 'place': item[3], 'price': item[1], 'href': item[5], 'tag': item[4],
                 'square': item[2],
                 'img_src': item[6], 'source': item[7], 'houseId': item[8], 'floor': item[9], 'scale': item[10],
                 'direction': item[11]} for item in result]

            # print(items_dict)
            return jsonify(items_dict)
        else:
            print("无数据")
            return jsonify({'error': 'No data found'}), 404  # 返回404状态码和错误信息
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
    # openId = request.args.get('openid')
    # print(openId)
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
            # print(favoriteMap)
            return jsonify(favoriteMap)

    except Exception as e:
        print(f"An error occurred in judgeStore: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/refresh', methods=['POST'])
def refresh():
    platform = request.json.get('platform')
    if platform == "ziRu":
        sql_all = 'SELECT href FROM house_info WHERE source = "自如"'
        sql_platform = 'SELECT href FROM ziru'
    elif platform == "lianJia":
        sql_all = 'SELECT href FROM house_info WHERE source = "链家"'
        sql_platform = 'SELECT href FROM lianjia'
    elif platform == "woAiWoJia":
        sql_all = 'SELECT href FROM house_info WHERE source = "我爱我家"'
        sql_platform = 'SELECT href FROM woaiwojia'
    elif platform == "all":
        sql_all = 'SELECT href FROM house_info '
        sql_platform = """SELECT woaiwojia.`href`
                        FROM woaiwojia
                        UNION ALL
                        SELECT ziru.`href`
                        FROM ziru
                        UNION ALL
                        SELECT lianjia.`href`
                        FROM lianjia;"""
    else:
        return jsonify({'error': "platform参数错误"})
    sql_all = 'SELECT href FROM house_info WHERE source = "自如"'
    sql_platform = 'SELECT href FROM ziru'
    cursor.execute(sql_all)
    allResult = cursor.fetchall()
    cursor.execute(sql_platform)
    platformResult = cursor.fetchall()
    platform_list = [t[0] for t in platformResult]
    all_list = [t[0] for t in allResult]
    for item in all_list:
        if item not in platform_list:
            print(item)
            sql = 'LOCK TABLES house_info WRITE;DELETE FROM house_info WHERE href = %s ;UNLOCK TABLES;'
            cursor.execute(sql, item)
    return jsonify({'success': 'successfully refresh'})


@app.route('/getName', methods=['POST'])
def getName():
    openId = request.json.get('openid')
    # openId = request.args.get('openid')
    print(openId)
    if not openId:
        return jsonify({'error': 'Missing openId'}), 400
    sql = 'SELECT name FROM admin WHERE openId=%s'
    try:
        cursor.execute(sql, openId)
        result = cursor.fetchone()
        return jsonify({'name': result})

    except Exception as e:
        print(f"An error occurred in getName: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
