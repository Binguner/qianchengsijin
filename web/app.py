from flask import Flask,render_template,request,g,jsonify
import flask
import json
from datetime import datetime

import read_data
import pandas as pd

app = Flask(__name__)


@app.route('/')
def page_index():
    return render_template('index.html')


@app.route('/search', methods=["GET", "POST"])
def page_search():
    if request.method == "POST":
        print('post')
        return render_template('search.html')
    else:
        print('get')
        return render_template('search.html')


@app.route('/ciyun')
def page_ciyun():
    return render_template('ciyun.html')

@app.route('/add_recruitment')
def page_add_job():
    return render_template('add_recruitment.html')


@app.route('/searchzw', methods=['POST'])
def get_ans():
    zhiweis = request.values.get("search_keyword")
    city = request.values.get("city_name")
    print('zhiweis is :' + zhiweis + ", city name is :" + city)
    zw = read_data.collection.find({"pname": {'$regex': zhiweis}})
    # print(str(zw))
    res = []
    for x in zw:
        res.append({'id': str(x['_id']), 'cname': x['cname'], 'pname': x['pname'], 'workplace':x['workplace'], 'welfare': x['welfare'],
                    'salary': x['salary'], 'education': x['education'], 'experience': x['experience'], 'requirement': x['requirement'],
                    'ctype': x['ctype'], 'scale': x['scale'], 'nature': x['nature'], 'dlink': x['dlink']})
    return jsonify(res)


@app.route('/get_ciyun', methods=['POST'])
def get_ciyun_data():
    res = 'no data'
    response = []
    try:
        with open("/Users/binguner/PycharmProjects/qianjin/web/static/ciyun_data.txt", 'r', encoding='utf-8') as f:
            res = f.read()
    finally:
        if f:
            f.close()
    # print(res)
    json_data = json.loads(res, encoding='utf-8')
    # print(json_data)
    for k,v in json_data.items():
        response.append({'name':k,'value':v})
        # print(k+" : " + str(v))
    return jsonify(json_data)





# @app.route('/',methods=["POST","GET"])
# def hello_world():
#     if request.method == 'POST':
#         zhiweis = request.form.get("zhiwei")
#         zw = read_data.collection.find({"pname": {'$regex': zhiweis}})
#         g.zw = zw
#         return render_template("search.html")
#     else:
#         return render_template("index.html")
#
#
# @app.route('/ciyun/',methods=["POST","GET"])
# def ciyun():
#     if request.method == 'POST':
#         zhiweis = request.form.get("zhiwei")
#         zw = read_data.collection.find({"pname": {'$regex': zhiweis}})
#         g.zw = zw
#         return render_template("search.html")
#     else:
#         return render_template("ciyun.html")
#
#
# @app.route('/educate/',methods=["POST","GET"])
# def education():
#     if request.method=='POST':
#        zhiweis=request.form.get("zhiwei")
#        zw=read_data.collection.find({"pname":{'$regex': zhiweis}})
#        g.zw=zw
#        return render_template("search.html")
#     else:
#         g.master=read_data.master
#         g.doctor=read_data.doctor
#         g.undergraduate=read_data.count_undergraduate
#         g.others=read_data.others
#         g.unlimited=read_data.unlimited
#         g.college=read_data.college
#         g.time=datetime.now()
#         return render_template("education.html")
#
#
# @app.route("/experience/",methods=["POST","GET"])
# def work_experience():
#     if request.method=='POST':
#        zhiweis=request.form.get("zhiwei")
#        zw=read_data.collection.find({"pname":{'$regex': zhiweis}})
#        g.zw=zw
#        # print(zw)
#        # cname=[]
#        # pname=[]
#        # workplace=[]
#        # welfare=[]
#        # education=[]
#        # experience=[]
#        # requirement=[]
#        # ctype=[]
#        # scale=[]
#        # nature=[]
#        # dlink=[]
#        # for item in zw:
#        #     print(item)
#            # # print(item)
#            # # print(item["pname"],item["scale"])
#            # cname.append(item["cname"])
#            # workplace.append(item["workplace"])
#            # pname.append(item["pname"])
#            # welfare.append(item["welfare"])
#            # experience.append(item["experience"])
#            # education.append(item["education"])
#            # requirement.append(item["requirement"])
#            # ctype.append(item["ctype"])
#            # scale.append(item["scale"])
#            # nature.append(item["nature"])
#            # dlink.append(item["dlink"])
#        # print(cname)
#        # # print(zw["pname"])
#        # # for zhiwei in zw:
#        # #     print(zhiwei["pname"])
#        # #     zhiwei1=zhiwei["pname"]
#        # #     result = read_data.collection.find_one({'pname': zhiwei1})
#        # g.cname=cname
#        # g.workplace=workplace
#        # g.pname=pname
#        # g.welfare=welfare
#        # g.experience= experience
#        # g.education=education
#        # g.requirement=requirement
#        # g.ctype=ctype
#        # g.scale=scale
#        # g.dlink=dlink
#        # g.nature=nature
#        return render_template("search.html")
#     else:
#         g.unrestricted=read_data.unrestricted
#         g.one_year=read_data.one_year
#         g.three_year=read_data.three_year
#         g.five_year=read_data.five_year
#         return render_template("experience.html")


if __name__ == '__main__':
    app.run(debug=True)