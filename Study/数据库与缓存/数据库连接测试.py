from pymongo import MongoClient

# 如果运行在本机上，实例无需参数
client = MongoClient()

# 如果运行在其他服务器上，则需要使用uri来指定连接地址，如下：
# client = MongoClient('mongodb://kingname:123456@45.76.110.210:27019')
# 如果未设置权限，则可写为：
# client = MongoClient('mongodb://45.76.110.210:27019')

db_name = 'test'
col_name = 'crawler'
database = client[db_name]
collection = database[col_name]
data = {'id': 1, 'name': 'kingname', 'age': 20, 'salary': 999999}
more_data = [
    data,
    {'id': 2, 'name': 'jx', 'age': 22, 'salary': 756},
    {'id': 3, 'name': 'cyr', 'age': 23, 'salary': 5555},
    {'id': 123, 'name': 'xll', 'age': 22, 'salary': 234}
]
# collection.insert_one(data)
# collection.insert_many(more_data)

# collection.update_one({'age': 20},{'$set':{'salary': 123}})
# collection.delete_one({'name': 'kingname'})
# content = [x for x in collection.find({})]
content = [x for x in collection.distinct('age')]
# content = [x for x in collection.find({'age': {'$gte': 20}}, {'_id': 0, 'name': 1, 'salary': 1})]
# content = [x for x in collection.find({}).sort('age', 1)]
print(content)
collection.update_one({'age': 20},{'$set':{'salary': 123}})
print('finished')