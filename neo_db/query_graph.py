from neo_db.config import graph, CA_LIST, similar_words
from spider.show_profile import get_profile
import codecs
import os
import json
import base64

def query(name):
    data = graph.run(
    "match(p )-[r]->(n:Person{Name:'%s'}) return  p.Name,r.relation,n.Name,p.cate,n.cate\
        Union all\
    match(p:Person {Name:'%s'}) -[r]->(n) return p.Name, r.relation, n.Name, p.cate, n.cate" % (name,name)
    )

    data = list(data)
    return get_json_data(data)

def get_json_data(data):
    json_data={'data':[],"links":[]}
    d=[]
    
    
    for i in data:
        # print(i["p.Name"], i["r.relation"], i["n.Name"], i["p.cate"], i["n.cate"])
        d.append(i['p.Name']+"_"+i['p.cate'])
        d.append(i['n.Name']+"_"+i['n.cate'])
        d=list(set(d))
    name_dict={}
    count=0
    for j in d:
        j_array=j.split("_")
    
        data_item={}
        name_dict[j_array[0]]=count
        count+=1
        data_item['name']=j_array[0]
        data_item['category']=CA_LIST[j_array[1]]
        json_data['data'].append(data_item)
    for i in data:
   
        link_item = {}
        
        link_item['source'] = name_dict[i['p.Name']]
        
        link_item['target'] = name_dict[i['n.Name']]
        link_item['value'] = i['r.relation']
        json_data['links'].append(link_item)

    return json_data
# f = codecs.open('./static/test_data.json','w','utf-8')
# f.write(json.dumps(json_data,  ensure_ascii=False))
def get_KGQA_answer(array):
    data_array=[]
    for i in range(len(array)-2):
        if i==0:
            name=array[0]
        else:
            name=data_array[-1]['p.Name']
           
        data = graph.run(
            "match(p)-[r:%s{relation: '%s'}]->(n:Person{Name:'%s'}) return  p.Name,n.Name,r.relation,p.cate,n.cate" % (
                similar_words[array[i+1]], similar_words[array[i+1]], name)
        )
       
        data = list(data)
        data_array.extend(data)
        
        print("==="*36)
          
    return [get_json_data(data_array)]

def get_answer_profile(name):
    with open("./spider/images/"+"%s.jpg" % (str(name)), "rb") as image:
        base64_data = base64.b64encode(image.read())
        b = str(base64_data)
    return [get_profile(str(name)), b.split("'")[1]]
        
def add_neo_db(text):
    rela_array = text
    graph.run("MERGE(p: Person{cate:'%s',Name: '%s'})"%(rela_array[3],rela_array[0]))
    graph.run("MERGE(p: Person{cate:'%s',Name: '%s'})" % (rela_array[4], rela_array[1]))
    graph.run(
        "MATCH(e: Person), (cc: Person) \
        WHERE e.Name='%s' AND cc.Name='%s'\
        CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
        RETURN r" % (rela_array[0], rela_array[1], rela_array[2],rela_array[2])
    )
    return 0

def decoration(text):
    ans = query(text)
    ss = ""
    if len(ans['data']) == 0:
        return "无"
    strs = ans['data'][0]['name']
    strs_n = ans['links'][0]['value']
    for i in range(len(ans['data']) - 1):
        ss += ans['data'][i+1]['name'] + ','
    return text + '与' + strs + "的关系是" + strs_n + "同时和" + ss + "有关系"
