# s = "12.3㎡ | 31/33层 | 朝南"
# print(s.replace(" ", "").split('|'))
import pymysql
from flask import jsonify

# 连接数据库
db = pymysql.connect(host='localhost', user='root', password='root', db='rent_house')
cursor = db.cursor()
sql = 'SELECT houseId FROM store_info WHERE userId=%s'
openId = 'oWoWf5AO2X81wOjaQehQtSEK3Nr4'
try:
    cursor.execute(sql, openId)
    result = cursor.fetchall()
    favoriteMap = {}
    for item in result[:-1]:
        favoriteMap[item[0]] = True
    print(favoriteMap)
    print(type(favoriteMap))

except Exception as e:
    print(f"An error occurred: {e}")
    print({'error': str(e)}, 500)

