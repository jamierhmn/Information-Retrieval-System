from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter
#from num2words import num2words

#lets try:https://xplordat.com/2019/10/28/semantics-at-scale-bert-elasticsearch/

import nltk
import os
import string
import numpy as np
import copy
import pandas as pd
import pickle
import re
import math
import sklearn.datasets as skds

# %load_ext autotime
def Prep_dataset():
    title = "case_doc"
    alpha = 0.3
    folders = "/home/jamie/Downloads/case_doc"

    files_train = skds.load_files(folders,load_content=False)
   # print(files_train)
    dataset = files_train.filenames
    #print(dataset)
    return dataset

def print_doc(id):
    print(dataset[id])
    file = open(dataset[id][0], 'r', encoding='cp1250')
    text = file.read().strip()
    file.close()
  #  print(text)

def convert_lower_case(data):
    return np.char.lower(data)

def remove_stop_words(data):
    stop_words = stopwords.words('english')
    words = word_tokenize(str(data))
    new_text = ""
    for w in words:
        if w not in stop_words and len(w) > 1:
            new_text = new_text + " " + w
    return new_text

def remove_punctuation(data):
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    return data

def remove_apostrophe(data):
    return np.char.replace(data, "'", "")


def stemming(data):
    stemmer = PorterStemmer()

    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + stemmer.stem(w)
    return new_text

def convert_numbers(data):
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        try:
            w = num2words(int(w))
        except:
            a = 0
        new_text = new_text + " " + w
    new_text = np.char.replace(new_text, "-", " ")
    return new_text


def preprocess(data):
    data = convert_lower_case(data)
    data = remove_punctuation(data) #remove comma seperately
    data = remove_apostrophe(data)
    data = remove_stop_words(data)
    data = convert_numbers(data)
    data = stemming(data)
    data = remove_punctuation(data)
    data = convert_numbers(data)
    data = stemming(data) #needed again as we need to stem the words
    data = remove_punctuation(data) #needed again as num2word is giving few hypens and commas fourty-one
    data = remove_stop_words(data) #needed again as num2word is giving stop words 101 - one hundred and one
    return data


def process_text(dataset):
    processed_text = []
    processed_title = []
    N = len(dataset)
  #  print(dataset[:N])
    for i in dataset:
        file = open(i, 'r', encoding="utf8", errors='ignore')
        text = file.read().strip()
        file.close()

        processed_text.append(word_tokenize(str(preprocess(text))))
        processed_title.append(word_tokenize(str(preprocess(i[1]))))
        return processed_text,processed_title

def term_freq(processed_text,processed_title):
    DF = {}

    for i in range(N):
        tokens = processed_text[i]
        for w in tokens:
            try:
                DF[w].add(i)
            except:
                DF[w] = {i}

        tokens = processed_title[i]
        for w in tokens:
            try:
                DF[w].add(i)
            except:
                DF[w] = {i}
    for i in DF:
        DF[i] = len(DF[i])
    return DF
def doc_freq(word,DF):
    c = 0
    try:
        c = DF[word]
    except:
        pass
    return c

def inverse_document(DF):
    doc = 0

    tf_idf = {}

    for i in range(N):

        tokens = processed_text[i]

        counter = Counter(tokens + processed_title[i])
        words_count = len(tokens + processed_title[i])

        for token in np.unique(tokens):
            tf = counter[token] / words_count
            df = doc_freq(token,DF)
            i

            tf_idf[doc, token] = tf * idf

        doc += 1
    return tf_idf

def TF_final(tf_idf):
    for i in tf_idf:
        tf_idf[i] *= alpha
    for i in tf_idf_title:
        tf_idf[i] = tf_idf_title[i]


def matching_score(k, query,tf_idf):
    preprocessed_query = preprocess(query)
    tokens = word_tokenize(str(preprocessed_query))

    print("Matching Score")
    print("\nQuery:", query)
    print("")
    print(tokens)

    query_weights = {}

    for key in tf_idf:

        if key[1] in tokens:
            try:
                query_weights[key[0]] += tf_idf[key]
            except:
                query_weights[key[0]] = tf_idf[key]

    query_weights = sorted(query_weights.items(), key=lambda x: x[1], reverse=True)

    print("")

    l = []

    for i in query_weights[:10]:
        l.append(i[0])

    print(l)


def gen_vector(tokens):
    Q = np.zeros((len(total_vocab)))

    counter = Counter(tokens)
    words_count = len(tokens)

    query_weights = {}

    for token in np.unique(tokens):

        tf = counter[token] / words_count
        df = doc_freq(token)
        idf = math.log((N + 1) / (df + 1))

        try:
            ind = total_vocab.index(token)
            Q[ind] = tf * idf
        except:
            pass
    return Q

def cosine_sim(a, b):
    cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
    return cos_sim



def cosine_similarity(k, query):
    print("Cosine Similarity")
    preprocessed_query = preprocess(query)
    tokens = word_tokenize(str(preprocessed_query))

    print("\nQuery:", query)
    print("")
    print(tokens)

    d_cosines = []

    query_vector = gen_vector(tokens)

    for d in D:
        d_cosines.append(cosine_sim(query_vector, d))

    out = np.array(d_cosines).argsort()[-k:][::-1]

    print("")

    print(out)

    for i in out:
        print(i, dataset[i])

filename =Prep_dataset()
text,title=processed_text,processed_title = process_text(filename)
DF=term_freq(text,title)
tf_idf=inverse_document(DF)
tf_idf = TF_final(tf_idf)
matching_score(tf_idf)
Q = cosine_similarity(2, "The manager directly responsible for operations of the utility area in each mill is responsible for compliance with this standard.")