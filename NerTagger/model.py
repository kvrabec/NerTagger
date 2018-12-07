import pandas as pd
import numpy as np
from keras import optimizers
from keras.models import Model, Input, load_model
from keras.layers import (LSTM, Embedding, Dense, TimeDistributed, Dropout, Conv1D,
                          Bidirectional, concatenate, SpatialDropout1D, GlobalMaxPooling1D)

WORD_OUT_DIM = 20
CHAR_OUT_DIM = 10
VALIDATION_SPLIT = 0.1
CHAR_UNITS = 20
CHAR_DROPOUT = 0.5
CHAR_RET_SEQ = False
MAIN_DROPOUT = 0.6
MAIN_RET_SEQ = True
MAIN_UNITS = 50
SPATIAL_DROPOUT = 0.3

BATCH_SIZE = 16
EPOCH_COUNT = 20
LEARNING_RATE = 0.001
OPTIMIZER = optimizers.Adam(LEARNING_RATE)
LOSS = "sparse_categorical_crossentropy"
METRICS = ["acc"]

def train(X_word_tr, y_tr, X_char_tr, n_words, n_tags, n_chars, max_len, max_len_char, model_name = ""):
    # input and embedding for words
    word_in = Input(shape=(max_len,))
    emb_word = Embedding(input_dim=n_words + 2, output_dim=WORD_OUT_DIM,
                            input_length=max_len, mask_zero=True)(word_in)

    # input and embeddings for characters
    char_in = Input(shape=(max_len, max_len_char,))
    emb_char = TimeDistributed(Embedding(input_dim=n_chars + 2, output_dim=CHAR_OUT_DIM,
                                input_length=max_len_char, mask_zero=True))(char_in)
    # character LSTM to get word encodings by characters
    char_enc = TimeDistributed(LSTM(units=CHAR_UNITS, return_sequences=CHAR_RET_SEQ,
                                    recurrent_dropout=CHAR_DROPOUT))(emb_char)

    x = concatenate([emb_word, char_enc])
    x = SpatialDropout1D(SPATIAL_DROPOUT)(x)
    main_lstm = Bidirectional(LSTM(units=MAIN_UNITS, return_sequences=MAIN_RET_SEQ,
                                    recurrent_dropout=MAIN_DROPOUT))(x)
    out = TimeDistributed(Dense(n_tags + 1, activation="softmax"))(main_lstm)

    model = Model([word_in, char_in], out)

    model.compile(optimizer=OPTIMIZER, loss=LOSS, metrics=METRICS)
    history = model.fit([X_word_tr,
                        np.array(X_char_tr).reshape((len(X_char_tr), max_len, max_len_char))],
                        np.array(y_tr).reshape(len(y_tr), max_len, 1),
                        batch_size=BATCH_SIZE, epochs=EPOCH_COUNT, validation_split=VALIDATION_SPLIT, verbose=1)

    hist = pd.DataFrame(data = history.history).to_csv(model_name + ".csv",
                                                encoding="utf-8")
    if(model_name != "" ):
        model.save(model_name + ".h5")

def predict(X_word_te, X_char_te, y_te, max_len, max_len_char, idx2word, idx2tag, model_file_name = 'model1.h5'):
    model = load_model(model_file_name)
    y_pred = model.predict([X_word_te,
                        np.array(X_char_te).reshape((len(X_char_te),
                                                        max_len, max_len_char))])
    
    if len(y_te) != 0:
        i = 1925
        p = np.argmax(y_pred[i], axis=-1)
        print("{:15}||{:5}||{}".format("Word", "True", "Pred"))
        print(30 * "=")
        for w, t, pred in zip(X_word_te[i], y_te[i], p):
            if w != 0:
                print("{:15}: {:5} {}".format(idx2word[w], idx2tag[t], idx2tag[pred]))
    else:
        sentence_count = len(y_pred)
        for i in range(sentence_count):
            p = np.argmax(y_pred[i], axis=-1)
            for word, t in zip(X_word_te[i], p):
                if word != 0:
                    print(idx2word[word] + ' ' + idx2tag[t])

def set_parametars(learning_rate, char_dropout, spatial_dropout, main_dropout):
    global CHAR_DROPOUT
    global MAIN_DROPOUT
    global SPATIAL_DROPOUT
    global LEARNING_RATE
    
    CHAR_DROPOUT = char_dropout
    MAIN_DROPOUT = main_dropout
    SPATIAL_DROPOUT = spatial_dropout
    LEARNING_RATE = learning_rate
    