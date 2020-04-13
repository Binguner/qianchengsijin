from flask import Flask,render_template,request,g,jsonify, session, flash, url_for, redirect
from collections import Counter
import flask
import json
from datetime import datetime
import read_data
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'


@app.route('/')
def page_index():
    username = session.get('username', 'none')
    if username == 'none':
        return render_template('login.html')
    return render_template('index.html')


@app.route('/login')
def page_login():
    return render_template('login.html')


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


@app.route('/edu_column')
def page_edu_column():
    return render_template('education_column.html')


@app.route('/exp_column')
def page_exp_column():
    return render_template('experience_column.html')


@app.route('/map_data')
def page_map_data():
    return render_template('map_data.html')


@app.route('/user_info')
def page_user_info():
    userinfo = read_data.getUserInfo()
    username = userinfo['username']
    email = userinfo['email']
    phone = userinfo['phone']
    type = userinfo['type']
    g.username = userinfo['username']
    g.email = userinfo['email']
    g.phone = userinfo['phone']
    g.type = userinfo['type']
    print(username + " : " + email + " : " + phone + " : " + type)
    return render_template('user_info.html')


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


@app.route('/add_job_data', methods=['POST'])
def add_job():
    cname = request.values.get('cname')
    pname = request.values.get('pname')
    workplace = request.values.get('workplace')
    welfare = request.values.get('welfare')
    salary = request.values.get('salary')
    education = request.values.get('education')
    experience = request.values.get('experience')
    requirement = request.values.get('requirement')
    ctype = request.values.get('ctype')
    scale = request.values.get('scale')
    nature = request.values.get('nature')
    dlink = request.values.get('dlink')

    # print('cname: ' + cname)
    # print('pname: ' + pname)
    # print('workplace: ' + workplace)
    # print('welfare: ' + welfare)
    # print('salary: ' + salary)
    # print('education: ' + education)
    # print('experience: ' + experience)
    # print('requirement: ' + requirement)
    # print('ctype: ' + ctype)
    # print('scale: ' + scale)
    # print('nature: ' + nature)
    # print('dlink: ' + dlink)

    job_dict = {
        'cname': cname,
        'pname': pname,
        'workplace': workplace,
        'welfare': welfare,
        'salary': salary,
        'education': education,
        'experience': experience,
        'requirement': requirement,
        'ctype': ctype,
        'scale': scale,
        'nature': nature,
        'dlink': dlink
    }

    res = read_data.collection.insert(job_dict)
    print(res)

    response_data = {
        'status': 'ok',
        'id': str(res)
    }

    # print(response_data)
    return jsonify(response_data)


@app.route('/searchzw', methods=['POST'])
def get_ans():
    zhiweis = request.values.get("search_keyword")
    city = request.values.get("city_name")
    print('zhiweis is :' + zhiweis + ", city name is :" + city)
    zw = read_data.collection.find({"pname": {'$regex': zhiweis}})
    # print(str(zw))
    res = []
    for x in zw:
        res.append({'id': str(x['_id']), 'cname': x['cname'], 'pname': x['pname'], 'workplace': x['workplace'], 'welfare': x['welfare'],
                    'salary': x['salary'], 'education': x['education'], 'experience': x['experience'], 'requirement': x['requirement'],
                    'ctype': x['ctype'], 'scale': x['scale'], 'nature': x['nature'], 'dlink': x['dlink']})
    return jsonify(res)


@app.route('/get_edu_data')
def get_edu_data():
    data = {}
    dazhuan_query = {'education': '大专'}
    benke_query = {'education': '本科'}
    shuoshi_query = {'education': '硕士'}
    boshi_query = {'education': '博士'}
    dazhuan_data = read_data.collection.find(dazhuan_query)
    benke__data = read_data.collection.find(benke_query)
    shuoshi_data = read_data.collection.find(shuoshi_query)
    boshi_data = read_data.collection.find(boshi_query)
    counter = Counter()

    for c in dazhuan_data:
        counter['大专'] += 1
    for c in benke__data:
        counter['本科'] += 1
    for c in shuoshi_data:
        counter['硕士'] += 1
    for c in boshi_data:
        counter['博士'] += 1
    print(str(read_data.count_undergraduate))
    print(str(read_data.master))
    print(str(read_data.doctor))
    print(str(read_data.college))
    # print(str(counter))
    return jsonify(counter)


@app.route('/get_exp_data')
def get_exp_data():
    mresponse = {
        '不限': read_data.almost_year,
        '1-2年': read_data.one_year,
        '3-5年': read_data.three_year,
        '5年以上': read_data.five_year
    }
    # print(read_data.one_year)
    # print(read_data.three_year)
    # print(read_data.five_year)
    # print(read_data.almost_year)
    return jsonify(mresponse)


@app.route('/do_login', methods=['POST'])
def dologin():
    username = request.values.get('username')
    password = request.values.get('password')
    # print(username)
    # print(password)
    msg = "登陆成功"
    isOk = 0
    if not read_data.check_user(username, password):
        isOk = 1
        msg = '用户名或密码错误，请检查。'
    result = {
        'isOk': isOk,
        'msg': msg
    }
    if isOk == 0:
        # print('after check : '+ str(session['id']))
        session['username'] = request.values.get('username')
        session['userid'] = request.values.get('username')
    # {
    #   "isOk": 0,
    #   "msg": "登陆成功"
    # }
    return jsonify(result)


@app.route('/logout', methods=['post'])
def logout():
    # print("pop: " + str(session.pop('username', 'none')))
    response = {
        'poped': str(session.pop('username', 'none')),
    }
    return jsonify(response)


@app.route('/get_map_data', methods=['post'])
def get_map_data():
    # list(read_data.data['workplace'])
    datalist = list(read_data.data['workplace'])
    counter = Counter()
    for item in datalist:
        counter[item]+=1
    response_data = []
    for c in counter.keys():
        response_data.append({'name': c, 'value':counter[c]})
        # print(c + " : " + str(counter[c]))
    return jsonify(response_data)




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
