import json
import os
import random

def randomText(textArr):
    length = len(textArr)
    if length < 1:
        return ''
    if length == 1:
        return str(textArr[0])
    randomNumber = random.randint(0,length-1)

    data = []
    if randomNumber%2 == 0:
        data.append(textArr[randomNumber])
    else:
        data.append(textArr[randomNumber])
    return data

def recom():
    with open("recommended/num2web.json",'r',encoding="utf-8") as f:
        json_web = json.load(f)
    with open("recommended/dataset.txt", "r",encoding='utf-8') as f:  # 打开文件
        lines = f.readlines()
        data = []
        for line in lines:
            data.append(line)
    with open("recommended/nums_score.json",'r',encoding="utf-8") as f:
        json_num = json.load(f)
        
    num_none = -0.1
    num_click = 20
    data_f = []
    a = sorted(json_num.items(), key=lambda x: x[1], reverse=True)
    js_value = list(json_web.values())
    
    for i in range(min(len(a),24)):
        dase = randomText(js_value[i])
        try:
            if data[2*dase[0]] != 'None\n':
                data_f.append(data[2*dase[0]])
                data_f.append(data[2*dase[0]+1])
        except:
            print("err")
    return data_f
        
        
    
