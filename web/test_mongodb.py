import pymongo

myclient = pymongo.MongoClient('localhost', 27017)
dblist = myclient.database_names()

# 创建数据库
mydb = myclient['learn_pymongo']

# 创建集合
mycollect = mydb['test_collect']

mydic = [
    {
        # '_id': 1,
        'name': 'Binguner',
        'age': 12
    },
    {
        # '_id': 2,
        'name': 'Jack',
        'age': 32
    },
]

mydic2 = {
    'name': 'Binguner',
    'age': 12,
    'url': 'www.binguner.com'
}

# 插入数据
# x = mycollect.insert(mydic)
# print(x)

# for x in dblist:
    # print(x)

# print()

# for x in mydb.collection_names():
#     print(x)

# print(mycollect.find_one())

# query = {'name': 'Jack'}
# for x in mycollect.find(query):
    # print(x)


# 高级查询
# 读取 name 字段中第一个 ASCII 值大于「H」的数据
# myquery1 = {'name': {"$gt": "H"}}
# 读取 name 字段中第一字母为「R」的数据
# myquery2 = {'name': {"$regex": "^R"}}


# for x in mycollect.find().limit(3):
#     print(x)

query = {"name": {"$regex": '^B'}}
# newValues = {'$set': {'name': 'Test'}}

# mycollect.update(query, newValues)
# mycollect.remove(query, multi=False)
# mycollect.remove()
for x in mycollect.find().sort('name', 1):
    print(x)


