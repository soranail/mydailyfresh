from redis import StrictRedis

sr = StrictRedis(host='localhost',port=6379,db=0,password='hezhenyu')
result = sr.keys()
print(result)
