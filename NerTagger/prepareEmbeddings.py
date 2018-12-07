import pandas as pd
import numpy as np
from keras.preprocessing.sequence import pad_sequences
import json
from nltk.tokenize import word_tokenize, sent_tokenize
import os

class SentenceGetter(object):
    
        def __init__(self, data):
            self.n_sent = 1
            self.data = data
            self.empty = False
            agg_func = lambda s: [(w, p, t) for w, p, t in zip(s["Word"].values.tolist(),
                                                                s["POS"].values.tolist(),
                                                                s["Tag"].values.tolist())]
            self.grouped = self.data.groupby("Sentence #").apply(agg_func)
            self.sentences = [s for s in self.grouped]
    
        def get_next(self):
            try:
                s = self.grouped["Sentence: {}".format(self.n_sent)]
                self.n_sent += 1
                return s
            except:
                return None

embedding_folder = os.path.dirname(os.path.abspath(__file__)) + '\\embeddingData\\'
X_word_file = embedding_folder + "X_word"
X_char_file = embedding_folder +"X_char"
y_file = embedding_folder + "y"
json_data_file = embedding_folder + "testFile.json"
dataset_file = embedding_folder + "ner_dataset.csv"

X_word = []
X_char = []
y = []
n_words = 0
n_tags = 0
n_chars = 0
word2idx = {}
idx2word = {}
tag2idx = {}
idx2tag = {}
char2idx = {}
max_len = 75
max_len_char = 10

def get_unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def prepare_text_for_prediction(text):
    sentences = sent_tokenize(text)
    words_input = []
    char_input = []
    for sentence in sentences:
        sent_seq = []
        sent_words = []
        for word in word_tokenize(sentence):
            try:
                sent_words.append(word2idx[word])
            except:
                sent_words.append(word2idx.get("UNK"))
        for i in range(max_len):
            word_seq = []
            for j in range(max_len_char):
                try:
                    word_seq.append(char2idx.get(sentence[i][0][j]))
                except:
                    word_seq.append(char2idx.get("PAD"))
            sent_seq.append(word_seq)
        words_input.append(sent_words)
        char_input.append(np.array(sent_seq))

    words_input = pad_sequences(maxlen=max_len, sequences=words_input, value=word2idx["PAD"], padding='post', truncating='post')
    return words_input, char_input

if (os.path.isfile(X_word_file + ".npy") and os.path.isfile(X_char_file + ".npy") 
        and os.path.isfile(y_file + ".npy") and os.path.isfile(json_data_file)):
    X_word = np.load(X_word_file + ".npy")
    X_char = np.load(X_char_file + ".npy")
    y = np.load(y_file + ".npy")
    with open(json_data_file) as file:
        data = json.load(file)
        n_words = data["n_words"]
        n_tags = data["n_tags"]
        n_chars = data["n_chars"]
        max_len = data["max_len"]
        max_len_char = data["max_len_char"]
        word2idx = data["word2idx"]
        idx2word = {i: w for w, i in word2idx.items()}
        tag2idx = data["tag2idx"]
        idx2tag = {i: w for w, i in tag2idx.items()}
        char2idx = data["char2idx"]
else:
    data = pd.read_csv(dataset_file, encoding="latin1")
    data = data.fillna(method="ffill")

    words = get_unique(data["Word"].values)
    n_words = len(words); n_words
    tags = get_unique(data["Tag"].values)
    n_tags = len(tags); n_tags

    getter = SentenceGetter(data)

    sentences = getter.sentences

    word2idx = {w: i + 2 for i, w in enumerate(words)}
    word2idx["UNK"] = 1
    word2idx["PAD"] = 0
    idx2word = {i: w for w, i in word2idx.items()}
    tag2idx = {t: i + 1 for i, t in enumerate(tags)}
    tag2idx["PAD"] = 0
    idx2tag = {i: w for w, i in tag2idx.items()}

    X_word = [[word2idx[w[0]] for w in s] for s in sentences]
    X_word = pad_sequences(maxlen=max_len, sequences=X_word, value=word2idx["PAD"], padding='post', truncating='post')
    chars = get_unique([w_i for w in words for w_i in w])
    n_chars = len(chars)

    char2idx = {c: i + 2 for i, c in enumerate(chars)}
    char2idx["UNK"] = 1
    char2idx["PAD"] = 0

    for sentence in sentences:
        sent_seq = []
        for i in range(max_len):
            word_seq = []
            for j in range(max_len_char):
                try:
                    word_seq.append(char2idx.get(sentence[i][0][j]))
                except:
                    word_seq.append(char2idx.get("PAD"))
            sent_seq.append(word_seq)
        X_char.append(np.array(sent_seq))

    y = [[tag2idx[w[2]] for w in s] for s in sentences]
    y = pad_sequences(maxlen=max_len, sequences=y, value=tag2idx["PAD"], padding='post', truncating='post')

    np.save(X_word_file,X_word)
    np.save(X_char_file,X_char)
    np.save(y_file,y)

    with open(json_data_file, "w") as file:
        d = {
            "n_words" : n_words,
            "n_tags" : n_tags,
            "n_chars" : n_chars,
            "max_len" : max_len,
            "max_len_char" : max_len_char,
            "word2idx" : word2idx,
            "tag2idx" : tag2idx,
            "char2idx" : char2idx
            }
        json.dump(d, file)