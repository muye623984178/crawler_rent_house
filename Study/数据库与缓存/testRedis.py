import redis

# 连接Redis
client = redis.StrictRedis(decode_responses=True)

# client.lpush('chapter', 123)
# print(client.llen('chapter'))
# print(client.lpop('chapter'))

# client.sadd('url', 'www.baidu.com')
# url = client.spop('url')
# length = client.scard('url')
# print(url)
# print(length)