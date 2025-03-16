import os
import faiss
import torch
import numpy as np
from sentence_transformers import SentenceTransformer

with open("recommended\\stop_word.txt", "r",encoding='utf-8') as f:
    datas = f.readlines()

stop_vec = []
for i in range(len(datas)):
    s = ""
    for j in datas[i]:
        if j != '\n':
            s += j
    stop_vec.append(s)

dir_path = 'recommended\\knowledge'
file_path = []
for dirpath, dirnames, filenames in os.walk(dir_path):
    for text_i in filenames:
        file_path.append('recommended\\knowledge\\' + text_i)

text_prm = []

for file_name in file_path:
    with open(file_name,encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        s = ""
        for line_k in line:
            if line_k != '\n' and line_k != ' ' and line_k != '#' and line_k != '，':
                s += line_k
        for sk in stop_vec:
            s.replace(sk,'')
        if len(s) > 15:
            text_prm.append(s)

prompt_index = faiss.read_index('recommended\\similarity\\large.index')
MODEL = 'recommended\\sentence-transformers_all-MiniLM-L6-v2'
#MODEL = 'bge-small-faiss'
MAX_LENGTH = 512
BATCH_SIZE = 16
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer(MODEL, device=device)
model.max_seq_length = MAX_LENGTH
def same(ss):
    string_wen = []
    string_wen.append(ss)
    question_data = np.array(string_wen)
    question_embeddings = model.encode(question_data, batch_size=BATCH_SIZE, device=device, show_progress_bar=True,
                                    convert_to_tensor=True, normalize_embeddings=True)
    question_embeddings = question_embeddings.detach().cpu().numpy()
    NUM_SENTENCES_INCLUDE = 1

    dict_dww = {}
    prompt_index = faiss.read_index('recommended\\similarity\\large.index')


    context = ""
    ss, ii = prompt_index.search(question_embeddings, NUM_SENTENCES_INCLUDE)

    for _s, _i in zip(ss[0], ii[0]):
        if _s < 2:
            if _i < len(text_prm) - 1:
                context += text_prm[_i] + '\n'
            else:
                context += text_prm[_i] + '\n'
    return(context)