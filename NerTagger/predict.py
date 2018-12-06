import numpy as np
from keras.models import load_model

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
            print('###')

