import os
import pickle as pk
import re
from string import punctuation

import numpy as np
from navec import Navec
from pymystem3 import Mystem
from razdel import tokenize, sentenize

import doc_file_worker

m = Mystem()

doc_files = doc_file_worker.get_doc_files()
print("finished stemming")
path = 'resources/navec_hudlit_v1_12B_500K_300d_100q.tar'
navec = Navec.load(path)
print("loaded navec")


def kl_preprocess(sent):
    sent = sent.lower()
    res = re.findall('[а-яё]+', sent)
    tmp_sent = ""
    for i in res:
        tmp_sent += i
        tmp_sent += ' '
    tmp_sent = tmp_sent.rstrip()
    return tmp_sent


def kl_stemming(text):
    return ''.join(m.lemmatize(text))


def kl_tokenize(sentence):
    tokens = [_.text for _ in list(tokenize(sentence))]
    res = [token for token in tokens if token not in punctuation]
    return res


def embed(text):
    res = []
    tokens = kl_tokenize(text)
    for token in tokens:
        if token in navec:
            res.append(navec[token])

    if not res:
        res.append(navec['<unk>'])

    return np.mean(res, axis=0)


def create_embeddings(option, emb_path):
    with open("resources/doc_text/" + doc_files[option] + ".txt", mode='r', encoding="utf-8") as f:
        contents = f.read()
    lst = [_.text for _ in list(sentenize(contents))]
    print("sentenized")
    print(lst[0])
    new_lst = []

    for sent in lst:
        new_lst.append(kl_preprocess(sent))

    stemmed_lst = []

    for el in new_lst:
        print(el)
        stemmed_lst.append(kl_stemming(el))

    embedded_data = [(embed(stemmed_lst[i]), i) for i in range(len(stemmed_lst))]
    pk.dump(embedded_data, open(emb_path, 'wb'))
    return embedded_data


def get_embeddings(option):
    emb_path = f'resources/embeddings/{doc_files[option]}.bin'
    if os.path.exists(emb_path):
        return pk.load(open(emb_path, 'rb'))
    return create_embeddings(option, emb_path)
