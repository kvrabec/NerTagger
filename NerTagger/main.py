import os
import sys
import model
from sklearn.model_selection import train_test_split
from prepareEmbeddings import (prepare_text_for_prediction,X_word, X_char,
                     n_words, n_tags, n_chars, max_len, max_len_char,
                     word2idx, idx2word, tag2idx, idx2tag, char2idx)

os.environ["TF_CPP_MIN_LOG_LEVEL"]="4"
model_file_name = os.path.dirname(os.path.abspath(__file__)) + '\\model1.h5'

print(model_file_name)

if not os.path.exists(model_file_name) or not os.path.isfile(model_file_name):
    X_word_tr, X_word_te, y_tr, y_te = train_test_split(X_word, y, test_size=0.1, random_state=2018)
    X_char_tr, X_char_te, _, _ = train_test_split(X_char, y, test_size=0.1, random_state=2018)
    model.train(X_word_tr, y_tr, X_char_tr, n_words, n_tags, n_chars, max_len, max_len_char, model_file_name)
    model.predict(X_word_te, X_char_te, y_te, max_len, max_len_char, idx2word, idx2tag, model_file_name)

if len(sys.argv) < 2:
    raise AttributeError("Enter text for tagging!")
text = sys.argv[1]
word_input, char_input = prepare_text_for_prediction(text)
model.predict(word_input, char_input, [], max_len, max_len_char, idx2word, idx2tag, model_file_name)