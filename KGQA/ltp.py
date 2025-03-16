# -*- coding: utf-8 -*-
import pyltp 
import os
LTP_DATA_DIR = 'KGQA/ltp_data'  # ltp模型目录的路径


def cut_words(words):
    seg_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
    segmentor = pyltp.Segmentor(seg_model_path)
    words = segmentor.segment(words)
    array_str="|".join(words)
    array=array_str.split("|")
    segmentor.release()
    return array


def words_mark(array):

    # 词性标注模型路径，模型名称为`pos.model`
    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
    postagger = pyltp.Postagger(pos_model_path)  # 初始化实例
    postags = postagger.postag(array)  # 词性标注
    pos_str=' '.join(postags)
    pos_array=pos_str.split(" ")
    postagger.release()  # 释放模型
    return pos_array

def get_target_array(words):
    target_pos=['ws','nh','n','nt','nr','nz']
    target_array=[]
    seg_array=cut_words(words)
    pos_array = words_mark(seg_array)
    for i in range(len(pos_array)):
        if pos_array[i] in target_pos:
            target_array.append(seg_array[i])
    return target_array

def get_total_array(words):
    target_pos_zhuanyou = ['nz']
    target_pos_didian = ['nl','ni','ns']
    target_pos_ren = ['nh']
    target_pos_shuo = ['i','j']
    target_pos_sijian = ['nt']
    target_pos_qita = ['n']
    target_pos_shijian = []
    
    target_array=[]
    target_pos_array = []
    seg_array=cut_words(words)
    pos_array = words_mark(seg_array)
    print(pos_array)
    for i in range(len(pos_array)):
        if pos_array[i] in target_pos_zhuanyou:
            target_array.append(seg_array[i])
            target_pos_array.append("专业名词")
        elif pos_array[i] in target_pos_didian:
            target_array.append(seg_array[i])
            target_pos_array.append("地点")
        elif pos_array[i] in target_pos_ren:
            target_array.append(seg_array[i])
            target_pos_array.append("人物")
        elif pos_array[i] in target_pos_shuo:
            target_array.append(seg_array[i])
            target_pos_array.append("名词缩写")
        elif pos_array[i] in target_pos_sijian:
            target_array.append(seg_array[i])
            target_pos_array.append("时间")
        elif pos_array[i] in target_pos_qita:
            target_array.append(seg_array[i])
            target_pos_array.append("其他")
        elif pos_array[i] in target_pos_shijian:
            target_array.append(seg_array[i])
            target_pos_array.append("事件")
    target = []
    target.append(target_array)
    target.append(target_pos_array)
    return target
        

def get_number(words):
    try:
        number = words_mark(words)
    except:
        number = "none"
    return number

def get_cut_list(text):
    js = []
    dist = {}
    ss = ""
    for i in text:
        if text[i] == 'A' or text[i] == 'a':
            dist["question"] = ss
            continue
        elif text[i] == 'B' or text[i] == 'b':
            dist["A"] = ss
            continue
        elif text[i] == 'C' or text[i] == 'c':
            dist["B"] = ss
            continue
        elif text[i] == 'D' or text[i] == 'd':
            dist["C"] = ss
            continue
        else:
            ss += text[i]
    js.append(dist)             
    return js


