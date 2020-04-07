from collections import Counter
import jieba
import read_data
import json


counter = Counter()
data = read_data.collection.find()
all_list = []
jieba.add_word("大数据")
jieba.add_word("大数据挖掘")

stop_words = ['(', ')', '：', '-', '（', '）', '/', '-', '+', ' ', '丨', 'k', '6300']
for item in data:
    list = jieba.lcut(item['pname'])
    # print(item['pname'])
    for i in list:
        if i not in stop_words:
            counter[i] += 1
        # all_list.append(i)

counter = counter.most_common(200)
    # print(c + " : " + str(counter[c]))

counter = dict(counter)

print(counter)
# print(str(counter)c)
# print(str(json.dumps(counter, ensure_ascii=False)))

with open("/Users/binguner/PycharmProjects/qianjin/web/static/ciyun_data.txt", 'w', encoding='utf-8') as f:
    f.write(str(json.dumps(counter, ensure_ascii=False)))
    f.close()
