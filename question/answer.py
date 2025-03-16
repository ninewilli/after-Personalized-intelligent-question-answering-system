import json
from transformers import AutoTokenizer, AutoModel
# from peft import PeftModel
import os
import faiss
import torch
import os
import gc
import pandas as pd
import numpy as np
import re
from tqdm.auto import tqdm

tokenizer = AutoTokenizer.from_pretrained("question/ChatGLM2-6B/THUDM/chatglm2-6b", trust_remote_code=True)
ckpt_path = 'single_chatglm2'
ckpt_path1 = 'single_chatglm'
model_old = AutoModel.from_pretrained("question/ChatGLM2-6B/THUDM/chatglm2-6b",
                                  load_in_8bit=False, 
                                  trust_remote_code=True).cuda()

def question_ans(text):
    history = []
    response, historys = model_old.chat(tokenizer,'用中文详细的回答' + text, history=history)
    return response