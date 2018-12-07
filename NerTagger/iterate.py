import os
import json
import model
import graph
from sklearn.model_selection import train_test_split
from prepareEmbeddings import (prepare_text_for_prediction,X_word, X_char,y,
                     n_words, n_tags, n_chars, max_len, max_len_char,
                     word2idx, idx2word, tag2idx, idx2tag, char2idx)

iterate__data_dir = os.path.dirname(os.path.abspath(__file__)) + '\\iterationData\\'
model_parametars_file = iterate__data_dir + 'modelParametars.json'

if os.path.exists(model_parametars_file) and os.path.isfile(model_parametars_file):
    with open(model_parametars_file) as file:
        parametars = json.load(file)
else:
    raise FileNotFoundError('Parametars file not found at following location "' + model_parametars_file +'"')

base_model_name = 'test_model'
has_csv_file = False

for file in os.listdir(iterate__data_dir):
    if file.endswith('.csv'):
       has_csv_file = True
       try:
           graph_files = graph.try_get_graph_files(parametars, base_model_name, iterate__data_dir)
           break
       except FileNotFoundError:
           graph_files = []
           break
if not has_csv_file:
    graph_files = []

if len(graph_files) == 0:
    for par in parametars['training_properties']:
        char_dropout = par['CHAR_DROPOUT']
        main_dropout = par['MAIN_DROPOUT']
        spatial_dropout = par['SPATIAL_DROPOUT']
        learning_rate = par['LEARNING_RATE']

        X_word_tr, X_word_te, y_tr, y_te = train_test_split(X_word, y, test_size=0.1, random_state=2018)
        X_char_tr, X_char_te, _, _ = train_test_split(X_char, y, test_size=0.1, random_state=2018)

        postfix = ('_LR_' + str(learning_rate) + '_CD_' + str(char_dropout) + 
                   '_MD_' + str(main_dropout) + '_SD_' + str(spatial_dropout))
        model_name = base_model_name + postfix
        model_path = iterate__data_dir + model_name

        model.set_parametars(learning_rate, char_dropout, spatial_dropout, main_dropout)
        model.train(X_word_tr, y_tr, X_char_tr, n_words, n_tags, n_chars, max_len, max_len_char, model_path)

    graph_files = graph.try_get_graph_files(parametars, base_model_name, iterate__data_dir)

graph.draw_graphs(graph_files)