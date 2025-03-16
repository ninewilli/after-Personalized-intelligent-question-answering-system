from relation.code.LSTM import prepare_sequence,LSTM_CRF
import json
import codecs
import torch
from collections import deque
import collections
import pandas as pd
from relation.code.BiLSTM_ATT import BiLSTM_ATT
from torch.autograd import Variable
import numpy as np
import relation.spy as spy
from KGQA.ltp import get_total_array
from neo_db.add_json import add_json
relation2id = {}
with codecs.open('relation/model/relation2id.txt','r','utf-8') as input_data:
    for line in input_data.readlines():
        relation2id[line.split()[0]] = int(line.split()[1])
    input_data.close()
    #print relation2id
model_r = torch.load('relation/model/model_epoch.pkl')
id2relation = {}
for text in relation2id:
    id2relation[relation2id[text]] = text
datas = deque()
labels = deque()
positionE1 = deque()
positionE2 = deque()
count = []
for i in range(131):
    count.append(0)
total_data=0
ad = [' ','\u3000', '\n', '。', '？', '！', '，', '；', '：', '、', '《', '》', '“', '”', '‘', '’', '［', '］', '....', '......',
          '『', '』', '（', '）', '…', '「', '」', '\ue41b', '＜', '＞', '+', '\x1a', '\ue42b','1','2','3','4','5','6','7','8','9','0','-']

data_re = {}
data_res = {}
with codecs.open('relation/model/train.txt','r','utf-8') as tfc:
    for lines in tfc:
        line = lines.split()
        if count[relation2id[line[2]]] <1500:
            sentence = []
            index1 = line[3].index(line[0])
            position1 = []
            index2 = line[3].index(line[1])
            position2 = []
            for i,word in enumerate(line[3]):
                sentence.append(word)
                position1.append(i-index1)
                position2.append(i-index2)
                i+=1
            datas.append(sentence)
            labels.append(relation2id[line[2]])
            positionE1.append(position1)
            positionE2.append(position2)
        count[relation2id[line[2]]]+=1
        total_data+=1

collections.Iterable = collections.abc.Iterable
def flatten(x):
    result = []
    for el in x:
        if isinstance(x, collections.Iterable) and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


all_words = flatten(datas)
sr_allwords = pd.Series(all_words)
sr_allwords = sr_allwords.value_counts()

set_words = sr_allwords.index
set_ids = range(1, len(set_words)+1)
word2id = pd.Series(set_ids, index=set_words)
id2word = pd.Series(set_words, index=set_ids)

word2id["BLANK"]=len(word2id)+1
word2id["UNKNOW"]=len(word2id)+1
id2word[len(id2word)+1]="BLANK"
id2word[len(id2word)+1]="UNKNOW"
#print "word2id",id2word

all_words = flatten(datas)
sr_allwords = pd.Series(all_words)
sr_allwords = sr_allwords.value_counts()

set_words = sr_allwords.index
set_ids = range(1, len(set_words) + 1)
word2id = pd.Series(set_ids, index=set_words)
id2word = pd.Series(set_words, index=set_ids)

word2id["BLANK"] = len(word2id) + 1
word2id["UNKNOW"] = len(word2id) + 1
id2word[len(id2word) + 1] = "BLANK"
id2word[len(id2word) + 1] = "UNKNOW"

max_len = 50

def X_padding(words):
    ids = []
    for i in words:
        if i in word2id:
            ids.append(word2id[i])
        else:
            ids.append(word2id["UNKNOW"])
    if len(ids) >= max_len:
        return ids[:max_len]
    ids.extend([word2id["BLANK"]] * (max_len - len(ids)))

    return ids


def pos(num):
    if num < -40:
        return 0
    if num >= -40 and num <= 40:
        return num + 40
    if num > 40:
        return 80


def position_padding(words):
    words = [pos(i) for i in words]
    if len(words) >= max_len:
        return words[:max_len]
    words.extend([81] * (max_len - len(words)))
    return words

model = torch.load('relation/model/model_epoch1.pkl',map_location='cpu')
dating = ""

Data = []
if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

word_idx = []
relation_data = []
with open("relation/data/testt.json",encoding='utf-8') as inputData:
    for line in inputData:
        try:
            word_idx.append(json.loads(line.rstrip(';\n')))
        except ValueError:
            print ("Skipping invalid line {0}".format(repr(line)))
word_to_ix = word_idx[0]

with open("relation/data/taget_main.json",encoding='utf-8') as inputData:
    for line in inputData:
        try:
            Data.append(json.loads(line.rstrip(';\n')))
        except ValueError:
            print ("Skipping invalid line {0}".format(repr(line)))
data = Data[0]

with open("relation/data/target_relation.json",encoding='utf-8') as inputData:
    for line in inputData:
        try:
            relation_data.append(json.loads(line.rstrip(';\n')))
        except ValueError:
            print ("Skipping invalid line {0}".format(repr(line)))
relation_data = relation_data[0]


def get_rela(str_name):
    var = str_name
    sentence_in = prepare_sequence(var, word_to_ix).to(device)
    sentence = model(sentence_in)[1]
    s = ""
    s_list = []
    for i in range(len(var)):
        if sentence[i] == 0 or sentence[i] == 1:
            s+=var[i]
        else:
            if s!="":
                s_list.append(s)
                s = ""
    ss = ""
    for str_s in s_list:
        ss += str_s
        ss += "  "
    if ss == "":
        ss = "未找到有效实体"
    return ss



def get_re(main,object,str_ss):
    test_main = str_ss
    test_obj = object
    test_relat = main
    ss = test_main
    position1 = []
    position2 = []

    index1 = ss.index(test_relat)
    index2 = ss.index(test_obj)

    for i, word in enumerate(ss):
        position1.append(i - index1)
        position2.append(i - index2)
        i += 1

    sentence = []
    pos1 = []
    pos2 = []

    sentence.append(X_padding(ss))
    pos1.append(position_padding(position1))
    pos2.append(position_padding(position2))

    sentence = torch.tensor(sentence)
    pos1 = torch.tensor(pos1)
    pos2 = torch.tensor(pos2)

    sentence = Variable(sentence)
    pos1 = Variable(pos1)
    pos2 = Variable(pos2)
    y = model_r(sentence, pos1, pos2)
    y = np.argmax(y.data.numpy(), axis=1)
    return id2relation[y[0]]+'\n'


def file_search(name1,name2,verson):
    var = "archive/" + name1 + name2
    num_right = 0
    if name2 == '.pdf':
        spy.pdf_docx(var)
        spy.word("archive/" + name1+".docx")
        num_right = 1
    elif name2 == '.wps':
        spy.wps_train(var)
        num_right = 1
    elif name2 == '.docx':
        spy.word(var)
        num_right = 1
    elif name2 == '.ofd':
        spy.ofd_train(var)
        num_right = 1
    elif name2 == '.txt':
        spy.txt_train(var)
        num_right = 1
    else:
        return 0
    data_da = {}
    lsit = []
    if num_right == 1:
        fp = r"test.txt"
        with open(fp, "r", encoding='UTF-8') as f:
            all_line_contents: list = f.readlines()
            for i in all_line_contents:
                if i:
                    i = i.replace("\n", '')
                lsit.append(i)
    totle_app = []
    totle_str = []

    for i in lsit:
        s = ""
        for q in i:
            if q not in word_to_ix:
                continue
            s += q
        totle_str.append(s)
        totle_app.append(model(prepare_sequence(s, word_to_ix).to(device))[1])
    dict_sence = {}
    data_index = []
    for i in range(len(totle_app)):
        s = ""
        for j in range(len(totle_app[i])):
            if totle_app[i][j] != 2:
                s += totle_str[i][j]
            elif s != "":
                data_index.append(s)
                dict_sence[s] = totle_str[i]
                s = ""

    for i in data_index:
        if len(i) < 2:
            continue
        dd_d = 0
        for j in data_index:
            if len(j) < 2:
                continue
            dd_d = 1
        if dd_d == 0:
            continue
        if i not in data:
            data_da[i] = []
        qw = 0
        dw = 0
        for j in data_index:
            if dict_sence[i] != dict_sence[j]:
                continue
            if len(j) < 2:
                continue
            if dw > 2:
                break
            if qw == 1:
                dw += 1
                try:
                    data_da[i].append(j)
                except:
                    print(i)
            if i == j:
                qw = 1

    for k in data_da:
        vec = {}
        for j in range(len(data_da[k])):
            if data_da[k][j] not in vec:
                vec[data_da[k][j]] = 1
        finda = []
        for k_w in vec:
            finda.append(k_w)
        data_da[k] = finda
    for text in data_da:
        if len(text) > 6 or len(text) < 2:
            continue
        for tes in data_da[text]:
            if len(tes) <= 6 and len(tes) >= 2:
                text_1 = ""
                tes_1 = ""
                rela1 = ""
                for i in text:
                    if i != '\n':
                        text_1 += i
                for i in tes:
                    if i != '\n':
                        tes_1 += i
                rela = get_re(text_1,tes_1,dict_sence[text])
                for i in rela:
                    if i != '\n':
                        rela1 += i
                if len(get_total_array(text_1)[1]) != 0:
                    cla1 = get_total_array(text)[1][0]
                else:
                    cla1 = "其他"
                if len(get_total_array(tes_1)[1]) != 0:
                    cla2 = get_total_array(text)[1][0]
                else:
                    cla2 = "其他"
                add_json(rela1,text_1,tes_1,cla1,cla2,verson)
                text_s = text_1 + "," + tes_1 + "," + rela1 + "," + cla1 + "," + cla2 + "\n"
                with open("raw_data/relation.txt","a",encoding='utf-8') as f:
                    f.write(text_s)
                f.close()
    return 0

