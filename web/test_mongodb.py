import pymongo
import test_pyspark
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

# 简历集合
resume_collect = database_51job['resume']

# 公司数量集合
company_number_collect = database_51job['company_number']

# 公司行业数量集合
company_nature_collect = database_51job['company_nature']

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
    # type root, hr, hunter
    user_dic = {
        'username': 'root',
        'password': 'root',
        'email':'478718805@qq.com',
        'phone':'1212121212',
        'type':'0',
    }
    user_collect.insert(user_dic)


def add_user_hr():
    user_dic = {
        'username': 'first_hr',
        'password': 'root',
        'email': '478718806@qq.com',
        'phone': '1234322',
        'type': '1',
    }
    user_collect.insert(user_dic)


def add_user_job_hunter():
    user_dic = {
        'username': 'job_hunter',
        'password': 'root',
        'email': '478718806@qq.com',
        'phone': '1234322',
        'type': '2',
    }
    user_collect.insert(user_dic)


def delete_user_root():
    deleted_user_dic = {
        'username': 'root'
    }
    user_collect.remove(deleted_user_dic, multi=False)

def delete_all_user():
    deleted_user_dic = {
        'username': 'job_hunter'
    }
    user_collect.remove(deleted_user_dic, multi=False)
    pass


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


def delete_data():
    rquery =  {
        'salary':''
    }
    zhiwei_collect.remove(rquery, multi=True)


def deleta_resume():
    query = {
        "name": "赵朝元"
    }
    resume_collect.remove(query)


def spark_get_company_type_number():
    res = test_pyspark.get_company_type_number()
    res = dict(res)
    for i in res.keys():
        print(str(i) + " : " + str(res[i]))
        dic = {
            'company_type': str(i),
            'company_number': res[i]
        }
        company_number_collect.insert(dic)


def spark_get_company_nature_number():
    res = test_pyspark.get_company_nature_number()
    res = dict(res)
    for i in res.keys():
        print(str(i) + " : " + str(res[i]))
        dic = {
            'company_nature': str(i),
            'company_number': res[i]
        }
        company_nature_collect.insert(dic)


def deleteNature():
    company_nature_collect.drop()


if __name__ == '__main__':
    pass

    # deleteNature()
    # spark_get_company_nature_number()
    # delete_data()
    # delete_all_user()
    # for i in zhiwei_collect.find():
    #     print(i)
    # check_user('root', 'root')
    # delete_user_root()
    # select_user_root()
    # add_user_root()
    # delete_user_root()
    # add_user_hr()
    # add_user_job_hunter()
    # print_all_user()
    # print_all_database()
    # print_all_collections_in_51_job()