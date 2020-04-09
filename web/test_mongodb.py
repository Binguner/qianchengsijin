import pymongo
from bson import ObjectId

myclient = pymongo.MongoClient('localhost', 27017)
dblist = myclient.database_names()

# 51job:
#       user
#       zhiwei

# 打开 51job 数据库
database_51job = myclient['51job']

# 输出 51job 里所有的集合
# print(database_51job.collection_names())

# 职位集合
zhiwei_collect = database_51job['zhiwei']

# 用户集合
user_collect = database_51job['user']

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


# for x in mycollect.find().sort('name', 1):
#     print(x)

# 查看 zhiwei 表中的所有数据
# for i in zhiwei_collection.find():
#     print(i)


# delete_dic = {
#     'username': 'root'
# }
# user_collection.remove(delete_dic)

# for i in user_collection.find():
#     print(i)


def print_all_database():
    print(myclient.database_names())


def print_all_collections_in_51_job():
    collections = myclient['51job']
    print(collections.collection_names())


def add_user_root():
    user_dic = {
        'username': 'root',
        'password': 'root'
    }
    user_collect.insert(user_dic)


def delete_user_root():
    deleted_user_dic = {
        'username': 'root'
    }
    user_collect.remove(deleted_user_dic)


def print_all_user():
    for i in user_collect.find():
        print(i)


def select_user_root():
    query = {
        '_id': ObjectId('5e8e8872f932ce354fc9e127')
    }
    c = user_collect.find(query)
    for i in c:
        print(i)


def check_user(username, password):
    query = {
        'username': username,
        'password': password
    }
    # print(query)
    cur = user_collect.find(query)
    for item in cur:
        print(item)
    count = cur.collection.count()
    print(count)



if __name__ == '__main__':
    check_user('root', 'root')
    # select_user_root()
    # add_user_root()
    # delete_user_root()
    # print_all_user()
    # print_all_database()
    # print_all_collections_in_51_job()