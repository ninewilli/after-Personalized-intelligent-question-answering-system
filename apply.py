from flask import Flask, render_template, request, jsonify
from neo_db.query_graph import query,get_KGQA_answer,get_answer_profile,add_neo_db
from KGQA.ltp import get_target_array,get_number,get_total_array
import neo_db.creat_graph
from relation.code.BiLSTM_ATT import BiLSTM_ATT
from relation.code.LSTM import LSTM_CRF
from relation.reply import get_rela,get_re
from recommended.search import search_same
from recommended.same import same
from flask import Flask, render_template
from listen.main import speechRecorder,speechRecorder_out
from flask import request
import time
from listen.main import baidu_aip
from listen.listening import listen
from recommended.search_baike import search_baike
from flask_cors import CORS
import os
import json
#from question.ChatGLM6B.answer import question_ans
from neo_db.add_json import add_json
from relation.reply import file_search
from recommended.search import gouzhao
from recommended.recommend import recom

app = Flask(__name__)
data_dict = {}
verson = 1
with open("recommended/stop_word.txt", "r",encoding='utf-8') as f:  # 打开文件
    lines = f.readlines()
    for line in lines:
        line = line.rstrip('\n')
        data_dict[line] = 1

@app.route('/', methods=['GET', 'POST'])

@app.route("/recognize", methods=['GET', 'POST'])
def recognize():
    global verson
    data = listen()
    if data == "字幕by索兰娅":
        data = "无"
    name = data
    jsons = get_total_array(str(name))
    json_data = jsons[0]
    json_insert = jsons[1]
    vec = []
    for k in range(min(3,len(json_data))):
        for j in range(min(3,len(json_data))):
            if k < j:
                rel = get_re(json_data[k],json_data[j],name)
                text = []
                text.append(json_data[k])
                text.append(json_data[j])
                text.append(rel)
                text.append(json_insert[k])
                text.append(json_insert[j])
                num = add_neo_db(text)
                vec.append(text)
        with open("raw_data/relation.txt", "r",encoding='utf-8') as f:  # 打开文件
            lines = f.readlines()
        for vec_t in vec:
            add_json(vec_t[0],vec_t[1],vec_t[2],vec_t[3],vec_t[4],verson)
            text_s = vec_t[0] + "," + vec_t[1] + "," + vec_t[2] + "," + vec_t[3] + "," + vec_t[4] + "\n"
            if lines[-1] == text_s:
                continue
            with open("raw_data/relation.txt","w",encoding='utf-8') as f:
                f.write(text_s)
        

    text_add = same(name)
    name += ' '  + name + ' '
    with open("recommended/base.txt","w",encoding='utf-8') as f:
        f.write(name)
    with open("recommended/add.txt","w",encoding='utf-8') as f:
        f.write(text_add)
    search_same()
    with open("recommended/original_data.txt", "r",encoding='utf-8') as f:  # 打开文件
        lines = f.readlines()
        data = []
        for line in lines:
            data.append(line)

    return jsonify(data)

@app.route("/uploads",methods=['GET', 'POST'])
def uploads():
    global verson
    file = request.files.get('file')
    verson = verson
    
    var = file.filename
    trans = os.path.splitext(var)
    name1,name2 = trans
    
    file.save(os.path.join("archive", "event" + name2))
    file_search("event",name2,verson)
    
    
    return jsonify("1")

@app.route("/get_datanum",methods=['GET', 'POST'])
def get_datanum():
    verson = request.get_json(silent=True)["verson"]
    if verson == 1:  
        with open("static/first_data.json",'r',encoding="utf-8") as f:
            json_w = json.load(f)
    elif verson == 2:
        with open("static/second_data.json",'r',encoding="utf-8") as f:
            json_w = json.load(f)
    elif verson == 3:
        with open("static/third_data.json",'r',encoding="utf-8") as f:
            json_w = json.load(f)
    elif verson == 4:
        with open("static/forth_data.json",'r',encoding="utf-8") as f:
            json_w = json.load(f)
    elif verson == 5:
        with open("static/fifth_data.json",'r',encoding="utf-8") as f:
            json_w = json.load(f)
    elif verson == 6:
        with open("static/six_data.json",'r',encoding="utf-8") as f:
            json_w = json.load(f)
    
    nums = []
    for i in json_w["data"]:
        nums.append(i)
    print(nums)
    return jsonify(nums)

@app.route("/recommend_kehu",methods=['GET', 'POST'])
def recommend_kehu():
    data = recom()
    return jsonify(data)
    
@app.route("/get_dataset",methods=['GET', 'POST'])
def get_dataset():
    verson = request.get_json(silent=True)["verson"]
    if verson == 1:  
        with open("static/first_data.json",'r',encoding="utf-8") as f:
            json_w = json.load(f)
    elif verson == 2:
        with open("static/second_data.json",'r',encoding="utf-8") as f:
            json_w = json.load(f)
    elif verson == 3:
        with open("static/third_data.json",'r',encoding="utf-8") as f:
            json_w = json.load(f)
    elif verson == 4:
        with open("static/forth_data.json",'r',encoding="utf-8") as f:
            json_w = json.load(f)
    elif verson == 5:
        with open("static/fifth_data.json",'r',encoding="utf-8") as f:
            json_w = json.load(f)
    elif verson == 6:
        with open("static/six_data.json",'r',encoding="utf-8") as f:
            json_w = json.load(f)
    data = []
    for i in range(6):
        data.append(0)
        
    for i in json_w["data"]:
        try:
            data[i["category"]] += 1
        except:
            print(i["category"])

    return jsonify(data)

@app.route("/get_json",methods=['GET', 'POST'])
def get_json():
    verson = request.get_json(silent=True)["verson"]
    print(verson)
    if verson == 1:
        with open("static/first_data.json",'r',encoding="utf-8") as f:
            json_map = json.load(f)
    elif verson == 2:
        with open("static/second_data.json",'r',encoding="utf-8") as f:
            json_map = json.load(f)
    elif verson == 3:
        with open("static/third_data.json",'r',encoding="utf-8") as f:
            json_map = json.load(f)
    elif verson == 4:
        with open("static/forth_data.json",'r',encoding="utf-8") as f:
            json_map = json.load(f)
    elif verson == 5:
        with open("static/fifth_data.json",'r',encoding="utf-8") as f:
            json_map = json.load(f)
    elif verson == 6:
        with open("static/six_data.json",'r',encoding="utf-8") as f:
            json_map = json.load(f)
    
    return jsonify(json_map)

@app.route("/speech_out",methods=['GET', 'POST'])
def beginRecorder_out():
	begin  = time.time()
	speechRecorder_out.run()
	return "200"

# 结束录音
@app.route("/stopSpeech_out", methods=["GET", "POST"])
def stopRecorder_out():
	print("停止录音……")
	speechRecorder_out.stop()
	end = time.time()
	return "200"

@app.route("/speech",methods=['GET', 'POST'])
def beginRecorder():
	begin  = time.time()
	speechRecorder.run()
	return "200"

# 结束录音
@app.route("/stopSpeech", methods=["GET", "POST"])
def stopRecorder():
	print("停止录音……")
	speechRecorder.stop()
	end = time.time()
	return "200"

@app.route('/get_profile',methods=['GET','POST'])
def get_profile():
    name = request.args.get('character_name')
    json_data = get_answer_profile(name)
    return jsonify(json_data)

@app.route('/KHQA_answer', methods=['GET', 'POST'])
def KHQA_answer():
    data = request.json.get('name')
    
    answer = "1"
    return jsonify(answer)
    
@app.route('/PHQA_answer', methods=['GET', 'POST'])
def PHQA_answer():
    question = request.json.get('msgContent')
    text_add = same(question)
    question += ' '  + question + ' '
    with open("recommended/base.txt","w",encoding='utf-8') as f:
        f.write(question)
    with open("recommended/add.txt","w",encoding='utf-8') as f:
        f.write(text_add)
    search_same()
    with open("recommended/original_data.txt", "r",encoding='utf-8') as f:  # 打开文件
        lines = f.readlines()
        data = []
        for line in lines:
            data.append(line)
    
    answer = "4534534312"
    return jsonify(answer)



@app.route('/KGQA_answer', methods=['GET', 'POST'])
def KGQA_answer():
    question = request.get_json(silent=True)["name"]
    verson_num = request.get_json(silent=True)["verson"]
    str_ques = question
    json_data = get_target_array(str(question))
    daw = []
    baike = ""
    try:
        baike_s = search_baike(str(json_data[0]))
        
        q = baike_s.index(str(json_data[0]))
        ss = ""
        for i in range(750):
            if i >= q:
                ss += baike_s[i]
                if baike_s[i] == '。':
                    baike += ss
                    ss = ""
    except:
        print('err')
    
    daw.append(query(str(json_data[0])))
    daw.append(question)
    daw.append(str(json_data[0]))
    daw.append(baike)
    
    answer = ""
    #answer = question_ans(question)
    jsons = get_total_array(str(answer))
    json_data = jsons[0]
    json_insert = jsons[1]
    for k in range(min(3,len(json_data))):
        for j in range(min(3,len(json_data))):
            if k < j:
                rel = get_re(json_data[k],json_data[j],answer)
                text = []
                text.append(json_data[k])
                text.append(json_data[j])
                text.append(rel)
                text.append(json_insert[k])
                text.append(json_insert[j])
                num = add_neo_db(text)
    daw.append(answer)
    text_add = same(question)
    question += ' '  + question + ' '
    with open("recommended/base.txt","w",encoding='utf-8') as f:
        f.write(question)
    with open("recommended/add.txt","w",encoding='utf-8') as f:
        f.write(text_add)
    search_same()
    with open("recommended/original_data.txt", "r",encoding='utf-8') as f:  # 打开文件
        lines = f.readlines()
        data = []
        for line in lines:
            data.append(line)
    daw.append(data)
    data_bai = []
    for j in range(min(len(json_data)-1,3)):
        baike = ""
        baike_s = search_baike(str(json_data[j+1]))
        q = baike_s.index(str(json_data[j+1]))
        ss = ""
        for i in range(min(750,len(baike_s))):
            if i >= q:
                ss += baike_s[i]
                if baike_s[i] == '。' or baike_s == '.':
                    baike += ss
                    ss = ""
        data_bai.append(str(json_data[j+1]))
        data_bai.append(baike)
    daw.append(data_bai)

    if int(verson_num) == 1:
        with open("archive/first.txt","w",encoding='utf-8') as f:
            f.write(str_ques + '\n')
            f.write("1"+'\n')
            f.write(answer + '\n')
            f.write("2"+'\n')
    elif int(verson_num) == 2:
        with open("archive/second.txt","w",encoding='utf-8') as f:
            f.write(str_ques + '\n')
            f.write("1"+'\n')
            f.write(answer + '\n')
            f.write("2"+'\n')
    elif int(verson_num) == 3:
        with open("archive/third.txt","w",encoding='utf-8') as f:
            f.write(str_ques + '\n')
            f.write("1"+'\n')
            f.write(answer + '\n')
            f.write("2"+'\n')
    elif int(verson_num) == 4:
        with open("archive/forth.txt","w",encoding='utf-8') as f:
            f.write(str_ques + '\n')
            f.write("1"+'\n')
            f.write(answer + '\n')
            f.write("2"+'\n')
    elif int(verson_num) == 5:
        with open("archive/fifth.txt","w",encoding='utf-8') as f:
            f.write(str_ques + '\n')
            f.write("1"+'\n')
            f.write(answer + '\n')
            f.write("2"+'\n')
    else:
        with open("archive/six.txt","w",encoding='utf-8') as f:
            f.write(question + '\n')
            f.write("1"+'\n')
            f.write(answer + '\n')
            f.write("2"+'\n')
    return jsonify(daw)

@app.route('/DXQA_answer', methods=['GET', 'POST'])
def DXQA_answer():
    question = request.get_json(silent=True)["name"]
    verson_num = request.get_json(silent=True)["verson"]
    str_ques = question
    json_data = get_target_array(str(question))
    daw = []
    baike = ""
    try:
        baike_s = search_baike(str(json_data[0]))
        q = baike_s.index(str(json_data[0]))
        ss = ""
        for i in range(750):
            if i >= q:
                ss += baike_s[i]
                if baike_s[i] == '。':
                    baike += ss
                    ss = ""
    except:
        print('err')
    
    daw.append(query(str(json_data[0])))
    daw.append(question)
    daw.append(str(json_data[0]))
    daw.append(baike)
    
    answer = ""
    #answer = question_ans(question)
    jsons = get_total_array(str(answer))
    json_data = jsons[0]
    json_insert = jsons[1]
    for k in range(min(3,len(json_data))):
        for j in range(min(3,len(json_data))):
            if k < j:
                rel = get_re(json_data[k],json_data[j],answer)
                text = []
                text.append(json_data[k])
                text.append(json_data[j])
                text.append(rel)
                text.append(json_insert[k])
                text.append(json_insert[j])
                num = add_neo_db(text)
    daw.append(answer)
    text_add = same(question)
    question += ' '  + question + ' '
    with open("recommended/base.txt","w",encoding='utf-8') as f:
        f.write(question)
    with open("recommended/add.txt","w",encoding='utf-8') as f:
        f.write(text_add)
    search_same()
    with open("recommended/original_data.txt", "r",encoding='utf-8') as f:  # 打开文件
        lines = f.readlines()
        data = []
        for line in lines:
            data.append(line)
    daw.append(data)
    data_bai = []
    for j in range(min(len(json_data)-1,3)):
        baike = ""
        baike_s = search_baike(str(json_data[j+1]))
        q = baike_s.index(str(json_data[j+1]))
        ss = ""
        for i in range(min(750,len(baike_s))):
            if i >= q:
                ss += baike_s[i]
                if baike_s[i] == '。' or baike_s == '.':
                    baike += ss
                    ss = ""
        data_bai.append(str(json_data[j+1]))
        data_bai.append(baike)
    daw.append(data_bai)

    if int(verson_num) == 1:
        with open("archive/first.txt","w",encoding='utf-8') as f:
            f.write(str_ques + '\n')
            f.write("1"+'\n')
            f.write(answer + '\n')
            f.write("2"+'\n')
    elif int(verson_num) == 2:
        with open("archive/second.txt","w",encoding='utf-8') as f:
            f.write(str_ques + '\n')
            f.write("1"+'\n')
            f.write(answer + '\n')
            f.write("2"+'\n')
    elif int(verson_num) == 3:
        with open("archive/third.txt","w",encoding='utf-8') as f:
            f.write(str_ques + '\n')
            f.write("1"+'\n')
            f.write(answer + '\n')
            f.write("2"+'\n')
    elif int(verson_num) == 4:
        with open("archive/forth.txt","w",encoding='utf-8') as f:
            f.write(str_ques + '\n')
            f.write("1"+'\n')
            f.write(answer + '\n')
            f.write("2"+'\n')
    elif int(verson_num) == 5:
        with open("archive/fifth.txt","w",encoding='utf-8') as f:
            f.write(str_ques + '\n')
            f.write("1"+'\n')
            f.write(answer + '\n')
            f.write("2"+'\n')
    else:
        with open("archive/six.txt","w",encoding='utf-8') as f:
            f.write(question + '\n')
            f.write("1"+'\n')
            f.write(answer + '\n')
            f.write("2"+'\n')
    return jsonify(daw)



@app.route('/search_name', methods=['GET', 'POST'])
def search_name():
    name = request.get_json(silent=True)["name"]
    json_data=query(str(name))
    return jsonify(json_data)

@app.route('/get_relation', methods=['GET', 'POST'])
def get_relation():
    name = request.get_json(silent=True)["name"]
    if name == "" :
        json_data = "未找到有效实体"
    else:
        json_data=get_rela(name)
    return jsonify(json_data)

@app.route('/get_add', methods=['GET', 'POST'])
def get_add():
    name = request.get_json(silent=True)["name"]
    verson = request.get_json(silent=True)["verson"]
    name_obj = request.get_json(silent=True)['name_obj']
    name_text = request.get_json(silent=True)['name_text']
    name_sty = get_number(name)
    name_obj_sty = get_number(name_sty)
    text = []
    text.append(name)
    text.append(name_obj)
    text.append(name_text)
    text.append(get_total_array(name)[1][0])
    text.append(get_total_array(name_obj)[1][0])
    num = add_neo_db(text)
    add_json(text[2],text[0],text[1],text[3],text[4],verson)
    text_s = text[0] + "," + text[1] + "," + text[2] + "," + text[3] + "," + text[4] + "\n"
    with open("raw_data/relation.txt","a",encoding='utf-8') as f:
        f.write(text_s)
    return jsonify([str(num)])
    
@app.route('/TSQA_answer', methods=['GET', 'POST'])
def TSQA_answer():
    question = request.get_json(silent=True)["name"]
    verson_num = request.get_json(silent=True)["verson"]
    str_ques = question
    json_data = get_target_array(str(question))
    daw = []
    baike = ""
    try:
        baike_s = search_baike(str(json_data[0]))
        q = baike_s.index(str(json_data[0]))
        ss = ""
        for i in range(750):
            if i >= q:
                ss += baike_s[i]
                if baike_s[i] == '。':
                    baike += ss
                    ss = ""
    except:
        print('err')
    daw.append(query(str(json_data[0])))
    daw.append(question)
    daw.append(str(json_data[0]))
    daw.append(baike)
    
    answer = ""
    #answer = question_ans(question)
    jsons = get_total_array(str(answer))
    json_data = jsons[0]
    json_insert = jsons[1]
    for k in range(min(3,len(json_data))):
        for j in range(min(3,len(json_data))):
            if k < j:
                rel = get_re(json_data[k],json_data[j],answer)
                text = []
                text.append(json_data[k])
                text.append(json_data[j])
                text.append(rel)
                text.append(json_insert[k])
                text.append(json_insert[j])
                num = add_neo_db(text)
    daw.append(answer)
    text_add = same(question)
    question += ' '  + question + ' '
    with open("recommended/base.txt","w",encoding='utf-8') as f:
        f.write(question)
    with open("recommended/add.txt","w",encoding='utf-8') as f:
        f.write(text_add)
    search_same()
    with open("recommended/original_data.txt", "r",encoding='utf-8') as f:  # 打开文件
        lines = f.readlines()
        data = []
        for line in lines:
            data.append(line)
    daw.append(data)
    data_bai = []
    for j in range(min(len(json_data)-1,3)):
        baike = ""
        baike_s = search_baike(str(json_data[j+1]))
        q = baike_s.index(str(json_data[j+1]))
        ss = ""
        for i in range(min(750,len(baike_s))):
            if i >= q:
                ss += baike_s[i]
                if baike_s[i] == '。' or baike_s == '.':
                    baike += ss
                    ss = ""
        data_bai.append(str(json_data[j+1]))
        data_bai.append(baike)
    daw.append(data_bai)

    if int(verson_num) == 1:
        with open("archive/first.txt","w",encoding='utf-8') as f:
            f.write(str_ques + '\n')
            f.write("1"+'\n')
            f.write(answer + '\n')
            f.write("2"+'\n')
    elif int(verson_num) == 2:
        with open("archive/second.txt","w",encoding='utf-8') as f:
            f.write(str_ques + '\n')
            f.write("1"+'\n')
            f.write(answer + '\n')
            f.write("2"+'\n')
    elif int(verson_num) == 3:
        with open("archive/third.txt","w",encoding='utf-8') as f:
            f.write(str_ques + '\n')
            f.write("1"+'\n')
            f.write(answer + '\n')
            f.write("2"+'\n')
    elif int(verson_num) == 4:
        with open("archive/forth.txt","w",encoding='utf-8') as f:
            f.write(str_ques + '\n')
            f.write("1"+'\n')
            f.write(answer + '\n')
            f.write("2"+'\n')
    elif int(verson_num) == 5:
        with open("archive/fifth.txt","w",encoding='utf-8') as f:
            f.write(str_ques + '\n')
            f.write("1"+'\n')
            f.write(answer + '\n')
            f.write("2"+'\n')
    else:
        with open("archive/six.txt","w",encoding='utf-8') as f:
            f.write(question + '\n')
            f.write("1"+'\n')
            f.write(answer + '\n')
            f.write("2"+'\n')
    return jsonify(daw)

    
@app.route('/PHrecommended', methods=['GET', 'POST'])
def PHrecommended():
    with open("recommended/original_data.txt", "r",encoding='utf-8') as f:  # 打开文件
        lines = f.readlines()
        data = []
        q = 0
        for line in lines:
            if line == 'None\n':
                q = 1
                continue
            if q == 1:
                q = 0
                continue
            data.append(line)
    return jsonify(data)

@app.route('/recommended', methods=['GET', 'POST'])
def recommended():
    name = request.get_json(silent=True)["name"]
    ls = get_target_array(name)

    data_jie = []
    for k in ls:
        if k not in data_dict:
            data_jie.append(k)
    data_ans = []
    for k in data_jie:
        baike = ""
        baike_s = search_baike(k)
        q = baike_s.index(k)
        ss = ""
        for i in range(750):
            if i >= q:
                ss += baike_s[i]
                if baike_s[i] == '。':
                    baike += ss
                    ss = ""
        data_ans.append(k + '\n')
        data_ans.append(baike)
        break
    
    with open("recommended/search_baike.txt","w",encoding='utf-8') as f:
        for k in data_ans:
            f.write(k)
    text_add = same(name)
    name += ' '  + name + ' '
    with open("recommended/base.txt","w",encoding='utf-8') as f:
        f.write(name)
    with open("recommended/add.txt","w",encoding='utf-8') as f:
        f.write(text_add)
    search_same()
    with open("recommended/original_data.txt", "r",encoding='utf-8') as f:  # 打开文件
        lines = f.readlines()
        data = []
        for line in lines:
            data.append(line)
    for k in data_ans:
        data.append(k)
    return jsonify(data)

@app.route('/get_relax', methods=['GET', 'POST'])
def get_relax():
    name = request.get_json(silent=True)["name"]
    name_obj = request.get_json(silent=True)["name_obj"]
    name_text = request.get_json(silent=True)["name_text"]
    relax = get_re(name,name_obj,name_text)
    return jsonify(relax)

@app.route('/submit_archive', methods=['GET', 'POST'])
def submit_archive():
    verson_num = int(request.get_json(silent=True)["verson"])
    txt_w = []
    if verson_num == 1:
        f=open('archive/first.txt',encoding='utf-8')
        line = f.readline().strip() #读取第一行
        txt=[]
        txt.append(line)
        while line:  # 直到读取完文件
            line = f.readline().strip()  # 读取一行文件，包括换行符
            txt.append(line)
        f.close()  # 关闭文件
        robot = []
        user = []
        ss = ""
        for i in txt:
            if i == "1":
                user.append(ss)
                ss = ""
                continue
            if i == "2":
                robot.append(ss)
                ss = ""
                continue
            ss += i
        txt_w.append(user)
        txt_w.append(robot)
    if verson_num == 2:
        f=open('archive/second.txt',encoding='utf-8')
        line = f.readline().strip() #读取第一行
        txt=[]
        txt.append(line)
        while line:  # 直到读取完文件
            line = f.readline().strip()  # 读取一行文件，包括换行符
            txt.append(line)
        f.close()  # 关闭文件
        robot = []
        user = []
        ss = ""
        for i in txt:
            if i == "1":
                user.append(ss)
                ss = ""
                continue
            if i == "2":
                robot.append(ss)
                ss = ""
                continue
            ss += i
        txt_w.append(user)
        txt_w.append(robot)
    if verson_num == 3:
        f=open('archive/third.txt',encoding='utf-8')
        line = f.readline().strip() #读取第一行
        txt=[]
        txt.append(line)
        while line:  # 直到读取完文件
            line = f.readline().strip()  # 读取一行文件，包括换行符
            txt.append(line)
        f.close()  # 关闭文件
        robot = []
        user = []
        ss = ""
        for i in txt:
            if i == "1":
                user.append(ss)
                ss = ""
                continue
            if i == "2":
                robot.append(ss)
                ss = ""
                continue
            ss += i
        txt_w.append(user)
        txt_w.append(robot)
    if verson_num == 4:
        f=open('archive/forth.txt',encoding='utf-8')
        line = f.readline().strip() #读取第一行
        txt=[]
        txt.append(line)
        while line:  # 直到读取完文件
            line = f.readline().strip()  # 读取一行文件，包括换行符
            txt.append(line)
        f.close()  # 关闭文件
        robot = []
        user = []
        ss = ""
        for i in txt:
            if i == "1":
                user.append(ss)
                ss = ""
                continue
            if i == "2":
                robot.append(ss)
                ss = ""
                continue
            ss += i
        txt_w.append(user)
        txt_w.append(robot)
    if verson_num == 5:
        f=open('archive/fifth.txt',encoding='utf-8')
        line = f.readline().strip() #读取第一行
        txt=[]
        txt.append(line)
        while line:  # 直到读取完文件
            line = f.readline().strip()  # 读取一行文件，包括换行符
            txt.append(line)
        f.close()  # 关闭文件
        robot = []
        user = []
        ss = ""
        for i in txt:
            if i == "1":
                user.append(ss)
                ss = ""
                continue
            if i == "2":
                robot.append(ss)
                ss = ""
                continue
            ss += i
        txt_w.append(user)
        txt_w.append(robot)
    if verson_num == 6:
        f=open('archive/six.txt',encoding='utf-8')
        line = f.readline().strip() #读取第一行
        txt=[]
        txt.append(line)
        while line:  # 直到读取完文件
            line = f.readline().strip()  # 读取一行文件，包括换行符
            txt.append(line)
        f.close()  # 关闭文件
        robot = []
        user = []
        ss = ""
        for i in txt:
            if i == "1":
                user.append(ss)
                ss = ""
                continue
            if i == "2":
                robot.append(ss)
                ss = ""
                continue
            ss += i
        txt_w.append(user)
        txt_w.append(robot)
    return jsonify(txt_w)

@app.route('/delete_file', methods=['GET', 'POST'])
def delete_file():
    verson_num = int(request.get_json(silent=True)["verson"])
    if int(verson_num) == 1:
        with open("archive/first.txt","w",encoding='utf-8') as f:
            f.write("")
    elif int(verson_num) == 2:
        with open("archive/second.txt","w",encoding='utf-8') as f:
            f.write("")
    elif int(verson_num) == 3:
        with open("archive/third.txt","w",encoding='utf-8') as f:
            f.write("")
    elif int(verson_num) == 4:
        with open("archive/forth.txt","w",encoding='utf-8') as f:
            f.write("")
    elif int(verson_num) == 5:
        with open("archive/fifth.txt","w",encoding='utf-8') as f:
            f.write("")
    else:
        with open("archive/six.txt","w",encoding='utf-8') as f:
            f.write("")
    return jsonify([])


CORS(app, resources=r'/*', supports_credentials=True)

if __name__ == '__main__':
    gouzhao()
    
    app.debug=True
    app.run(host='0.0.0.0',port='5000')
