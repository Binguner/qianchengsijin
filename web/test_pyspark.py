import os
import re
from pyspark.sql import SparkSession,Row
from pyspark import SparkContext
from operator import add
import findspark


os.environ['PYSPARK_PYTHON'] = '/usr/bin/python3'
input_uri = "mongodb://127.0.0.1:27017/51job.zhiwei"
output_uri = "mongodb://127.0.0.1:27017/51job.zhiwei"

my_spark = SparkSession \
    .builder \
    .appName("MyApp") \
    .config("spark.mongodb.input.uri", input_uri) \
    .config("spark.mongodb.output.uri", output_uri) \
    .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.11:2.2.0') \
    .getOrCreate()

df = my_spark.read.format('com.mongodb.spark.sql.DefaultSource').load()


collection = df.rdd


def get_city_job_number():
    map_ans = collection.map(lambda x: (x.asDict()['workplace'], 1)).countByKey()
    # reduceByKey会寻找相同key的数据，当找到这样的两条记录时会对其value(分别记为x,y)
    # map_ans2 = collection.map(lambda x: (x.asDict()['workplace'], 1)).reduceByKey(lambda x,y:x+y)
    return dict(map_ans)


def get_company_type_number():
    company_count = collection.map(lambda x: (x.asDict()['ctype'],1)).countByKey()
    return dict(company_count)


def get_company_nature_number():
    company_count = collection.map(lambda x: (x.asDict()['nature'],1)).countByKey()
    return dict(company_count)


def get_education_data():
    education_list = ['大专', '本科', '硕士', '博士']
    ans = collection.map(lambda x: (x.asDict()['education'], 1)).filter(lambda x: x[0] in education_list).countByKey()
    return dict(ans)


def get_experience_data():
    exp_keys = ['不限', '1-2年', '3-4年', '5-7年', '8-9年', '10年以上']
    data_list = ['3-4年', '1年', '2年', '5-7年', '在校生/应届生', '无需', '10年以上', '8-9年']
    data = dict(collection\
        .map(lambda x: (x.asDict()['experience'], 1))\
        .filter(lambda x: x[0] in data_list).countByKey())
    no_limit = data['在校生/应届生'] + data['无需']
    one_two = data['1年'] + data['2年']
    three_four = data['3-4年']
    five_seven = data['5-7年']
    eight_nine = data['8-9年']
    more_ten = data['10年以上']
    res = {
        '不限': no_limit,
        '1-2年': one_two,
        '3-4年': three_four,
        '5-7年': five_seven,
        '8-9年': eight_nine,
        '10年以上': more_ten
    }
    # print(data)
    return res
    # print('no_limit：' + str(no_limit) + '\n' + 'one_two：' + str(one_two) + '\n' + 'three_four ：' + str(three_four)
    #       + '\n' + 'five_seven: ' + str(five_seven) + '\n' + 'eight_nine : ' + str(eight_nine) + "\n" + 'more_ten：' + str(more_ten))


def get_ciyun_jobs():
    res = collection.map(lambda x: (x.asDict()['pname'], 1)).countByKey()
    print(res)


# get_ciyun_jobs()
# get_experience_data()
# aaa = collection.map(lambda x: (x.asDict()['experience'], 1)).countByKey()
# print(aaa)

# for i in collection.collect():
#     print(i['experience'] + " ： " + i['education'])
# [('10年以上', 109)
# , ('1年', 946),
# ('2年', 948),
# ('3-4年', 1555),
# ('5-7年', 1021),
# ('8-9年', 161),
# ('中专', 48),
# ('中技', 9),
# ('初中及以下', 3),
# ('博士', 8),
# '在校生/应届生', 2804),
# '大专', 527),
# '招100人', 2),
# '招10人', 48),
# '招11人', 1),
# '招12人', 2),
# '招15人', 5),
# '招16人', 1),
# '招18人', 53),
# '招1人', 125),
# '招20人', 65),
# '招2人', 82),
# '招30人', 15),
# '招33人', 1),
# '招3人', 51),
# '招4人', 17),
# '招50人', 3),
# '招5人', 170),
# '招6人', 22),
# '招7人', 5),
# '招8人', 31),
# '招9人', 2),
# '招若干人', 308),
# '无需', 1150),
# '本科', 937),
# ('硕士', 26),
# ('高中', 248)]



# collection.distinct().countByKey().items()

# collection.foreach(fun)

# print(type(collection))


# words = my_spark

# sc = SparkContext('local', 'FirstApp')
# words = sc.parallelize([
#     "scala",
#     "java",
#     "hadoop",
#     "spark",
#     "akka",
#     "pyspark",
#     'pyspark vs spark',
#     "pyspark and spark"
# ])
#

# print('collect is : ' + str(collect.collect()))

# nums = sc.parallelize([1, 2, 3, 4, 5])
# adding = nums.reduce(add)
# print('adding : ' + str(adding))
#

# x = sc.parallelize([('hadoop', 1), ('spark', 2)])
# y = sc.parallelize([('hadoop', 2), ('spark', 3)])
# joined = x.join(y)
# final = joined.collect()
# print(final )

# 返回RDD中的元素个数
# count = df.count()
# print('count is ' + count)

# 返回RDD中的所有元素
# collect = df.collect()
# 打印第一条数据
# print(collect[0])

# foreach(func) 仅返回满足foreach内函数条件的元素
# print(collect[0]['cname'])
# print(collect)


# array = []
# def getData(x):
#     dic = x.asDict()
#     # print((dic['workplace'],dic['salary']))
#     # print('add')
#     # re.findall('\d+', 'asd234sad565')
#     array.append((dic['workplace'], re.findall(r'\d+', str(dic['salary']))))
#     # print('added')
#
#
# # df.foreach(getData)
# # df.collect.foreach(array.append((_.asDict['workplace'],_.asDict['salary'])))
# # df.foreach(lambda x:array.append((x.asDict['workplace'],x.asDict['salary'])))
# # df.foreach(lambda x:array.append((x.asDict['workplace'],x.asDict['salary'])))
#
# array = []
# for item in df.collect():
#     temp = item.asDict()
#     number = float(re.findall('\d+',temp['salary'])[0])
#     if number != 0.0:
#         array.append((temp['workplace'], number))
# print(array)
#
# data = my_spark.sparkContext.parallelize(array)
#
# data1 = data.aggregateByKey((0,0),lambda x,y:(x[0]+y,x[1]+1),lambda x,y:(x[0]+y[0],x[1]+y[1]))
#
# data2 = data1.map(lambda x:(x[0],x[1][0]/x[1][1]))
#
# print(data2.collect())
# for item in data2.collect():
#     print(item)
# # print(coll)
#
#
# # print('count: ' + str(count))
# # print('collect: ' + str(collect))
