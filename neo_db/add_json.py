import json

with open("static/first_data.json",'r',encoding="utf-8") as f:
    json_w = json.load(f)
num = 0
data_dict = {}
data = []
data_links = json_w['links']
dict_num = {}
for test_tes in data_links:
    dict_num[str(test_tes["source"]) + "+" + str(test_tes['target'])] = 1

for test in json_w['data']:
    test_name = test['name']
    data_dict[test_name] = num
    num += 1
    data.append(test_name)

first_data = json_w
with open("static/second_data.json",'r',encoding="utf-8") as f:
    json_w = json.load(f)
num1 = 0
data_dict1 = {}
data1 = []
data_links1 = json_w['links']
dict_num1 = {}
for test_tes in data_links1:
    dict_num1[str(test_tes["source"]) + "+" + str(test_tes['target'])] = 1

for test in json_w['data']:
    test_name = test['name']
    data_dict1[test_name] = num1
    num1 += 1
    data1.append(test_name)    
second_data = json_w
with open("static/third_data.json",'r',encoding="utf-8") as f:
    json_w = json.load(f)
num2 = 0
data_dict2 = {}
data2 = []
data_links2 = json_w['links']
dict_num2 = {}
for test_tes in data_links2:
    dict_num2[str(test_tes["source"]) + "+" + str(test_tes['target'])] = 1

for test in json_w['data']:
    test_name = test['name']
    data_dict2[test_name] = num2
    num2 += 1
    data2.append(test_name)    

third_data = json_w
with open("static/forth_data.json",'r',encoding="utf-8") as f:
    json_w = json.load(f)
num3 = 0
data_dict3 = {}
data3 = []
data_links3 = json_w['links']
dict_num3 = {}
for test_tes in data_links3:
    dict_num3[str(test_tes["source"]) + "+" + str(test_tes['target'])] = 1

for test in json_w['data']:
    test_name = test['name']
    data_dict3[test_name] = num3
    num3 += 1
    data3.append(test_name)    
forth_data = json_w
with open("static/forth_data.json",'r',encoding="utf-8") as f:
    json_w = json.load(f)
num3 = 0
data_dict3 = {}
data3 = []
data_links3 = json_w['links']
dict_num3 = {}
for test_tes in data_links3:
    dict_num3[str(test_tes["source"]) + "+" + str(test_tes['target'])] = 1

for test in json_w['data']:
    test_name = test['name']
    data_dict3[test_name] = num3
    num3 += 1
    data3.append(test_name)    
fifth_data = json_w

with open("static/fifth_data.json",'r',encoding="utf-8") as f:
    json_w = json.load(f)
num4 = 0
data_dict4 = {}
data4 = []
data_links4 = json_w['links']
dict_num4 = {}
for test_tes in data_links4:
    dict_num4[str(test_tes["source"]) + "+" + str(test_tes['target'])] = 1

for test in json_w['data']:
    test_name = test['name']
    data_dict4[test_name] = num4
    num4 += 1
    data4.append(test_name)   
     
six_data = json_w
with open("static/six_data.json",'r',encoding="utf-8") as f:
    json_w = json.load(f)
num5 = 0
data_dict5 = {}
data5 = []
data_links5 = json_w['links']
dict_num5 = {}
for test_tes in data_links5:
    dict_num5[str(test_tes["source"]) + "+" + str(test_tes['target'])] = 1

for test in json_w['data']:
    test_name = test['name']
    data_dict5[test_name] = num5
    num5 += 1
    data5.append(test_name)    

nums = []
data_dicts = []
datas = []
data_linkss = []
dict_nums = []

nums.append(num)
nums.append(num1)
nums.append(num2)
nums.append(num3)
nums.append(num4)
nums.append(num5)

data_dicts.append(data_dict)
data_dicts.append(data_dict1)
data_dicts.append(data_dict2)
data_dicts.append(data_dict3)
data_dicts.append(data_dict4)
data_dicts.append(data_links5)

datas.append(data)
datas.append(data1)
datas.append(data2)
datas.append(data3)
datas.append(data4)
datas.append(data5)

data_linkss.append(data_links)
data_linkss.append(data_links1)
data_linkss.append(data_links2)
data_linkss.append(data_links3)
data_linkss.append(data_links4)
data_linkss.append(data_links5)

dict_nums.append(dict_num)
dict_nums.append(dict_num1)
dict_nums.append(dict_num2)
dict_nums.append(dict_num3)
dict_nums.append(dict_num4)
dict_nums.append(dict_num5)

map_data = []
map_data.append(first_data)
map_data.append(second_data)
map_data.append(third_data)
map_data.append(forth_data)
map_data.append(fifth_data)
map_data.append(six_data)

style = []
style.append("专业名词")
style.append("地点")
style.append("人物")
style.append("名词缩写")
style.append("时间")
style.append("其他")
style.append("事件")

def add_json(name,rela,obj,cla1,cla2,verson):
    verson = verson - 1
    num_ver = 0
    num_ob = 0
    nums_cla1 = 0
    nums_cla2 = 0
    for i in range(len(style)):
        if style[i] == cla1:
            nums_cla1 = i
        if style[i] == cla2:
            nums_cla2 = i
    if rela in data_dicts[verson]:
        num_ver = data_dicts[verson][rela]
    else:
        nums[verson] += 1
        num_ver = nums[verson]
        map_data[verson]['data'].append({'name':rela,'category':nums_cla1})
    
    if obj in data_dicts[verson]:
        num_ob = data_dicts[verson][obj]
    else:
        nums[verson] += 1
        num_ob = nums[verson]
        map_data[verson]['data'].append({'name':obj,'category':nums_cla2})
    
    if str(num_ver) + "+" + str(num_ob) not in dict_nums:
        map_data[verson]['links'].append({"source": num_ver-1, "target": num_ob-1, "value": name})
    if verson == 0:
        with open('static/first_data.json', 'w',encoding="utf-8") as file:
            json.dump(map_data[verson], file,ensure_ascii=False)
    elif verson == 1:
        with open('static/second_data.json', 'w',encoding="utf-8") as file:
            json.dump(map_data[verson], file,ensure_ascii=False)
    elif verson == 2:
        with open('static/third_data.json', 'w',encoding="utf-8") as file:
            json.dump(map_data[verson], file,ensure_ascii=False)
    elif verson == 3:
        with open('static/forth_data.json', 'w',encoding="utf-8") as file:
            json.dump(map_data[verson], file,ensure_ascii=False)
    elif verson == 4:
        with open('static/fifth_data.json', 'w',encoding="utf-8") as file:
            json.dump(map_data[verson], file,ensure_ascii=False)
    elif verson == 5:
        with open('static/six_data.json', 'w',encoding="utf-8") as file:
            json.dump(map_data[verson], file,ensure_ascii=False)
    return 0
