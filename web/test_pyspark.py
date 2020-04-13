import os
import re
import findspark
from pyspark.sql import SparkSession

findspark.init()

# set PYSPARK_PYTHON to python36
os.environ['PYSPARK_PYTHON'] = '/usr/bin/python3'

# load mongo data
input_uri = "mongodb://127.0.0.1:27017/51job.zhiwei"
output_uri = "mongodb://127.0.0.1:27017/51job.zhiwei"

my_spark = SparkSession \
    .builder \
    .appName("MyApp") \
    .config("spark.mongodb.input.uri", input_uri) \
    .config("spark.mongodb.output.uri", output_uri) \
    .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.11:2.2.0').getOrCreate()

df = my_spark.read.format('com.mongodb.spark.sql.DefaultSource').load()
# 返回RDD中的元素个数
count = df.count()
# 返回RDD中的所有元素
collect = df.collect()
print(collect[0])
# foreach(func) 仅返回满足foreach内函数条件的元素
# print(collect[0]['cname'])
# print(collect)


# dic1 = {'_id': Row(oid='5e8cb108f932ce1d8490bd79'), 'cname': '人生无限公司', 'ctype': '国企', 'dlink': 'Android工程师',
#         'education': '本科', 'experience': '1-3年', 'nature': '酒店/旅游', 'pname': 'Android工程师', 'requirement': '',
#         'salary': '19-29', 'scale': '100-200人', 'welfare': '五险一金,定期体检,交通补贴,餐饮补贴,通讯补贴,员工旅游', 'workplace': '福建-0-0'}
# androidcolle.append(dic1)

# array = []
def getData(x):
    dic = x.asDict()
    # print((dic['workplace'],dic['salary']))
    # print('add')
    # re.findall('\d+', 'asd234sad565')
    array.append((dic['workplace'], re.findall(r'\d+', str(dic['salary']))))
    # print('added')


# df.foreach(getData)
# df.collect.foreach(array.append((_.asDict['workplace'],_.asDict['salary'])))
# df.foreach(lambda x:array.append((x.asDict['workplace'],x.asDict['salary'])))
# df.foreach(lambda x:array.append((x.asDict['workplace'],x.asDict['salary'])))

array = []
for item in df.collect():
    temp = item.asDict()
    number = float(re.findall('\d+',temp['salary'])[0])
    if number != 0.0:
        array.append((temp['workplace'], number))
print(array)

data = my_spark.sparkContext.parallelize(array)

data1 = data.aggregateByKey((0,0),lambda x,y:(x[0]+y,x[1]+1),lambda x,y:(x[0]+y[0],x[1]+y[1]))

data2 = data1.map(lambda x:(x[0],x[1][0]/x[1][1]))

print(data2.collect())
for item in data2.collect():
    print(item)
# print(coll)


# print('count: ' + str(count))
# print('collect: ' + str(collect))
