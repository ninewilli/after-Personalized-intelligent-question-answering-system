import re
import requests
from lxml.html import etree
import time
import math
# 重定向输出结果到original_data.txt
import sys
import re   #筛选url
import requests  #请求
import os
import json
def gouzhao():
    index_num = 0
    word_num = 0
    web2json = {}
    web2num = {}
    with open("recommended/dataset.txt","w",encoding='utf-8') as f:
                f.write("")
    json_data = []
    with open("static/first_data.json",'r',encoding="utf-8") as f:
        json_w1 = json.load(f)
    ind_num = 0
    for i in json_w1['data']:
        if ind_num > 72:
            break
        ind_num += 1
        json_data.append(i['name'])
        
    with open("static/second_data.json",'r',encoding="utf-8") as f:
        json_w1 = json.load(f)
    ind_num = 0
    for i in json_w1['data']:
        if ind_num > 72:
            break
        ind_num += 1
        json_data.append(i['name'])
    with open("static/third_data.json",'r',encoding="utf-8") as f:
        json_w1 = json.load(f)
    ind_num = 0
    for i in json_w1['data']:
        if ind_num > 72:
            break
        ind_num += 1
        json_data.append(i['name'])
    with open("static/forth_data.json",'r',encoding="utf-8") as f:
        json_w1 = json.load(f)
    ind_num = 0
    for i in json_w1['data']:
        if ind_num > 72:
            break
        ind_num += 1
        json_data.append(i['name'])
    with open("static/fifth_data.json",'r',encoding="utf-8") as f:
        json_w1 = json.load(f)
    ind_num = 0
    for i in json_w1['data']:
        if ind_num > 72:
            break
        ind_num += 1
        json_data.append(i['name'])
    with open("static/six_data.json",'r',encoding="utf-8") as f:
        json_w1 = json.load(f)
    ind_num = 0
    for i in json_w1['data']:
        if ind_num > 72:
            break
        ind_num += 1
        json_data.append(i['name'])
    
    try:
        for json_text in json_data:
            web2num[word_num] = 0
            word_num += 1
            web2json[json_text] = []
            def get_bing_url(keywords):
                keywords = keywords.strip('\n')
                bing_url = re.sub(r'^', 'https://cn.bing.com/search?q=', keywords)
                bing_url = re.sub(r'\s', '+', bing_url)
                return bing_url


            base_keys = [json_text]
            
            for key in base_keys:
                word = key.strip()
                url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&logid=5853806806594529489&ipn=rj&ct=201326592&is=&fp=result&fr=ala&word={}&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&expermode=&nojc=&isAsync=&pn=30&rn=30&gsm=1e&1658411978178='.format(word, word)
                headers = {
                    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39'
                    }
                files='static/images'#创建文件夹路径
                if not os.path.exists(files): #假如没有文件执行以下代码：
                    os.makedirs(files) #有文件夹则覆盖，没有则创建
                #获取html源码
                response_html=requests.get(url=url,headers=headers)
                #正则提取图片
                result='"thumbURL":"(.*?)"' #正则式
                img_list=re.findall(result,response_html.text)  #筛选
                file_name=1 #使用数字命名
                for img_url in img_list: #遍历刷选后的网址        get_image(a,i) #将遍历后的url地址传到get-image这个函数
                    #发送请求 获取字节数据
                    response=requests.get(url=img_url,headers=headers)
                    #定义文件名和类型 创建的文件夹路径+文件名+类型
                    file=files + '/' + str(file_name)+'.png' 
                    #创建图片文件  写入二进制
                    with open(file,mode='wb') as f:
                        #写入字节数据
                        f.write(response.content)
                        #文件名+1 防止重复
                        file_name+=1
                    if file_name == 5:
                        break
                added_keys = [json_text] # add.txt contains the name of universities
                for t_key in added_keys:
                    key_n = ""
                    for i in range(min(int(len(key.strip())/3 + math.sqrt(len(t_key.strip()))),len(t_key.strip()))):
                        key_n += t_key.strip()[i]
                    new_key = key.strip()+key_n

                    bing_url = get_bing_url(new_key)

                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                            'Accept-Encoding': 'gzip, deflate',
                            'cookie': 'DUP=Q=sBQdXP4Rfrv4P4CTmxe4lQ2&T=415111783&A=2&IG=31B594EB8C9D4B1DB9BDA58C6CFD6F39; MUID=196418ED32D66077102115A736D66479; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=DDFFA87D3A894019942913899F5EC316&dmnchg=1; ENSEARCH=BENVER=1; _HPVN=CS=eyJQbiI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMC0wMy0xNlQwMDowMDowMFoiLCJJb3RkIjowLCJEZnQiOm51bGwsIk12cyI6MCwiRmx0IjowLCJJbXAiOjd9; ABDEF=V=13&ABDV=11&MRNB=1614238717214&MRB=0; _RwBf=mtu=0&g=0&cid=&o=2&p=&c=&t=0&s=0001-01-01T00:00:00.0000000+00:00&ts=2021-02-25T07:47:40.5285039+00:00&e=; MUIDB=196418ED32D66077102115A736D66479; SerpPWA=reg=1; SRCHUSR=DOB=20190509&T=1614253842000&TPC=1614238646000; _SS=SID=375CD2D8DA85697D0DA0DD31DBAB689D; _EDGE_S=SID=375CD2D8DA85697D0DA0DD31DBAB689D&mkt=zh-cn; _FP=hta=on; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; dsc=order=ShopOrderDefault; ipv6=hit=1614260171835&t=4; SRCHHPGUSR=CW=993&CH=919&DPR=1&UTC=480&WTS=63749850642&HV=1614256571&BRW=HTP&BRH=M&DM=0'
                            }
                    string_s = ""
                    for i in range(1,3):  # 通过for in来翻页
                        if i == 1:
                            url = bing_url
                        else:
                            url = bing_url + '&qs=ds&first=' + str((i * 10) - 1) + '&FORM=PERE'
                        content = requests.get(url=url, timeout=5, headers=headers)
                        # 获取content中网页的url
                        tree = etree.HTML(content.text)
                        try:
                            li = tree.xpath('//ol[@id="b_results"]//li[@class="b_algo"]')[0] # [0] query the first result
                        except Exception:
                            print('error')
                        
                        try:
                            h3 = li.xpath('//h2/a')
                            for h in h3:
                                if h.text == 'None':
                                    continue
                                result_url = h.attrib['href'] # 获取网页的url
                                text = h.text # 获取网页的标题
                                string_s += f'{text}' + '\n' + f'{result_url}' + '\n'
                                web2json[json_text].append(index_num)
                                index_num += 1
                        except Exception:
                            print('error')
            with open("recommended/dataset.txt","a",encoding='utf-8') as f:
                    f.write(string_s)
            js = json.dumps(web2json, ensure_ascii=False)  
            fileObject = open('recommended/num2web.json', 'w', encoding='utf-8')  
            fileObject.write(js+'\n')  
            fileObject.close()
            js = json.dumps(web2num, ensure_ascii=False)  
            fileObject = open('recommended/nums_score.json', 'w', encoding='utf-8')  
            fileObject.write(js+'\n')  
            fileObject.close()
            

    except:
        print(0)
    
    
def search_same():
    
    def get_bing_url(keywords):
        keywords = keywords.strip('\n')
        bing_url = re.sub(r'^', 'https://cn.bing.com/search?q=', keywords)
        bing_url = re.sub(r'\s', '+', bing_url)
        return bing_url


    base_keys = open('recommended\\base.txt', 'r', encoding='utf-8')
    
    for key in base_keys:
        word = key.strip()
        url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&logid=5853806806594529489&ipn=rj&ct=201326592&is=&fp=result&fr=ala&word={}&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&expermode=&nojc=&isAsync=&pn=30&rn=30&gsm=1e&1658411978178='.format(word, word)
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39'
            }
        files='static/images'#创建文件夹路径
        if not os.path.exists(files): #假如没有文件执行以下代码：
            os.makedirs(files) #有文件夹则覆盖，没有则创建
        #获取html源码
        response_html=requests.get(url=url,headers=headers)
        #正则提取图片
        result='"thumbURL":"(.*?)"' #正则式
        img_list=re.findall(result,response_html.text)  #筛选
        file_name=1 #使用数字命名
        for img_url in img_list: #遍历刷选后的网址        get_image(a,i) #将遍历后的url地址传到get-image这个函数
            #发送请求 获取字节数据
            response=requests.get(url=img_url,headers=headers)
            #定义文件名和类型 创建的文件夹路径+文件名+类型
            file=files + '/' + str(file_name)+'.png' 
            #创建图片文件  写入二进制
            with open(file,mode='wb') as f:
                #写入字节数据
                f.write(response.content)
                #文件名+1 防止重复
                file_name+=1
            if file_name == 5:
                break
        added_keys = open('recommended\\add.txt', 'r', encoding='utf-8') # add.txt contains the name of universities
        for t_key in added_keys:
            key_n = ""
            for i in range(min(int(len(key.strip())/3 + math.sqrt(len(t_key.strip()))),len(t_key.strip()))):
                key_n += t_key.strip()[i]
            new_key = key.strip()+key_n

            bing_url = get_bing_url(new_key)

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                    'Accept-Encoding': 'gzip, deflate',
                    'cookie': 'DUP=Q=sBQdXP4Rfrv4P4CTmxe4lQ2&T=415111783&A=2&IG=31B594EB8C9D4B1DB9BDA58C6CFD6F39; MUID=196418ED32D66077102115A736D66479; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=DDFFA87D3A894019942913899F5EC316&dmnchg=1; ENSEARCH=BENVER=1; _HPVN=CS=eyJQbiI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMC0wMy0xNlQwMDowMDowMFoiLCJJb3RkIjowLCJEZnQiOm51bGwsIk12cyI6MCwiRmx0IjowLCJJbXAiOjd9; ABDEF=V=13&ABDV=11&MRNB=1614238717214&MRB=0; _RwBf=mtu=0&g=0&cid=&o=2&p=&c=&t=0&s=0001-01-01T00:00:00.0000000+00:00&ts=2021-02-25T07:47:40.5285039+00:00&e=; MUIDB=196418ED32D66077102115A736D66479; SerpPWA=reg=1; SRCHUSR=DOB=20190509&T=1614253842000&TPC=1614238646000; _SS=SID=375CD2D8DA85697D0DA0DD31DBAB689D; _EDGE_S=SID=375CD2D8DA85697D0DA0DD31DBAB689D&mkt=zh-cn; _FP=hta=on; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; dsc=order=ShopOrderDefault; ipv6=hit=1614260171835&t=4; SRCHHPGUSR=CW=993&CH=919&DPR=1&UTC=480&WTS=63749850642&HV=1614256571&BRW=HTP&BRH=M&DM=0'
                    }
            string_s = ""
            for i in range(1,3):  # 通过for in来翻页
                if i == 1:
                    url = bing_url
                else:
                    url = bing_url + '&qs=ds&first=' + str((i * 10) - 1) + '&FORM=PERE'
                content = requests.get(url=url, timeout=5, headers=headers)
                # 获取content中网页的url
                tree = etree.HTML(content.text)
                try:
                    li = tree.xpath('//ol[@id="b_results"]//li[@class="b_algo"]')[0] # [0] query the first result
                except Exception:
                    print('error')
                
                try:
                    h3 = li.xpath('//h2/a')
                    for h in h3:
                        result_url = h.attrib['href'] # 获取网页的url
                        text = h.text # 获取网页的标题
                        string_s += f'{text}' + '\n' + f'{result_url}' + '\n'
                except Exception:
                    print('error')
    with open("recommended/original_data.txt","w",encoding='utf-8') as f:
            f.write(string_s)