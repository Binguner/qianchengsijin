import pymongo
from flask import g,session
from bson import ObjectId
import pandas as pd

# 连接数据库
client = pymongo.MongoClient('localhost', 27017)
# 选择 dbs
db = client['51job']
# 选中表
collection = db['zhiwei']
collection_user = db['user']
collection_resume = db['resume']



# 读取表中数据
data = pd.DataFrame(list(collection.find()))
# 选择需要显示的字段
data = data[['pname','cname',"workplace","education","salary","experience"]]
# print(list(data['pname']))

# 数据表基本信息（维度、列名称、数据格式、所占空间等）：
# print(data.info())

# 查看列名称
# print(data.columns)

# print(data.groupby('workplace').count())
# for x in collection.find({"pname": {'$regex': 'Android'}}):
#     print(x)

# 打印输出
data1=list(data['education'])
data2=list(data['experience'])

# print(data1)
# print(data2)

count_undergraduate=0
master=0
doctor=0
others=0
college=0
unlimited=0
unrestricted=0
graduate=0
one_year=0
almost_year=0
three_year=0
five_year=0
# g.teststr = 'ffef'

for data1 in data1:
    if data1=="本科":
        count_undergraduate=count_undergraduate+1
    elif data1=="硕士":
        master=master+1
    elif data1=="博士":
        doctor=doctor+1
    elif data1=="大专":
          college=college+1
    elif data1=="不限":
        unlimited=unlimited+1
    else:
        pass
for data2 in data2:
    if data2=="应届毕业生" or data2=="应届"or data2=="应届生":
        graduate=graduate+1
    elif data2=="不限":
        unrestricted=unrestricted+1
    elif data2=="1年"or data2=="2年"or data2=="1-2年":
        one_year=one_year+1
    elif data2=="3年"or data2=="4年"or data2=="3-4年":
        three_year=three_year+1
    elif data2=="5年"or data2=="6年"or data2=="5-7年" or data2=='8-9年':
        five_year=five_year+1
    elif data2=="一年以下" or data2=='无需':
        almost_year=almost_year+1
    else:
        pass
# print(count_undergraduate,master,doctor,college,unlimited)
# print(graduate,unrestricted,one_year,three_year,five_year,almost_year)


def check_user(username, password):
    query = {
        'username': username,
        'password': password
    }
    res = False
    # print(query)
    for c in collection_user.find(query):
        session['id'] = str(c['_id'])
        # print(c['username'])
        # print('id:'+str(c['_id']))
        if c['username'] == username:
            res = True
            print(res)
        # print(c['username'])
    # print(res)
    return res


def get_userid(username):
    query = {
        'username': username
    }
    cc = collection_user.find_one(query)
    return


def getUserInfo():
    userid = str(session['id'])
    query = {
        '_id': ObjectId(userid)
    }
    res = collection_user.find_one(query)
    # print('res ' + str(res))
    return res


def add_resume(data):
    print(data)
    collection_resume.insert(data)


def get_resume(id):
    query = {
        'id': id
    }
    res = collection_resume.find_one(query)
    return res




# print(list(data['workplace']))