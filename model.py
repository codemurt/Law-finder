import numpy as np
from pymystem3 import Mystem
from razdel import sentenize
from transformers import pipeline

import word2vector

m = Mystem()

doc_files = {"Конституция РФ": "constitution"}
qa_model = pipeline("question-answering", model="AlexKay/xlm-roberta-large-qa-multilingual-finedtuned-ru")


def get_answer(option, question):
    with open("resources/doc_text/" + doc_files[option] + ".txt", mode='r', encoding="utf-8") as f:
        contents = f.read()
    lst = [_.text for _ in list(sentenize(contents))]

    def cosine(u, v):
        res = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
        return res

    embedded_data = word2vector.get_embeddings(option)
    print("embedded data")
    indexes = set()

    def add_idx_to_set(idx):
        idx = int(idx)
        for i in range(idx - 2, idx + 3):
            if 0 < i < len(lst):
                indexes.add(i)

    def get_result(text):
        query = word2vector.embed(text)

        cosines = [(cosine(x[0], query), x[1]) for x in embedded_data]
        print("got cosines")

        vals = sorted(cosines, key=lambda x: x[0])
        for i in range(-1, -3, -1):
            idx_ans = int(vals[i][1])
            add_idx_to_set(idx_ans)

    question_emb = word2vector.kl_stemming(word2vector.kl_preprocess(question))
    print("preprocessed question")
    get_result(question_emb)

    def get_context(set_indexes):
        ctx = ""
        for el in set_indexes:
            ctx += lst[el]
        return ctx

    context = get_context(indexes)
    print("got context")
    print("start downloading")

    print("finish downloading")
    results = qa_model(question=question, context=context)

    indexes.clear()
    return results, context
