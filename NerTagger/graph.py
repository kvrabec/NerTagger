import matplotlib.pyplot as plt
import pandas as pd
import os

def try_get_graph_files(parametars, base_model_name, iterate__data_dir):
    graphFiles = []
    for index in range(7):
        start = index*3
        end = (index+1)*3
        files = []
        for par in parametars['training_properties'][start:end]:
            char_dropout = par['CHAR_DROPOUT']
            main_dropout = par['MAIN_DROPOUT']
            spatial_dropout = par['SPATIAL_DROPOUT']
            learning_rate = par['LEARNING_RATE']
            postfix = ('_LR_' + str(learning_rate) + '_CD_' + str(char_dropout) + 
                       '_MD_' + str(main_dropout) + '_SD_' + str(spatial_dropout))
            file_name = base_model_name + postfix
            file_path = iterate__data_dir + file_name + '.csv'
            if not os.path.exists(file_path):
                raise FileNotFoundError('File "' + file_path + '" not found')
            files.append({'file' : file_path,
                          'name' : 'Learning rate :' + str(learning_rate)})
        graphFiles.append({'files' : files,
                          'name' : 'Char dropout: ' + str(char_dropout) + ', Main dropout: ' + str(main_dropout) + ', Spatial dropout: ' + str(spatial_dropout)})
    return graphFiles

def draw_graphs(graph_files):
    for graph in graph_files:
        plt.style.use('ggplot')
        plt.figure(figsize=(12,12))
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        for file in graph['files']:
            data = pd.read_csv(file['file'])
            accuracy = data['acc']
            validation_accuracy = data['val_acc']
            accuracy.name = file['name'] + '_acc'
            validation_accuracy.name = file['name'] + '_val_acc'
            plt.plot(accuracy)
            plt.plot(validation_accuracy)
        plt.legend(loc=4)
        plt.title(graph['name'])
        plt.show()

def draw_training_graph(data_file):
     graphFile = ({
                    'files' : [{   
                                'file' : data_file,
                                'name' : 'Model'
                               }],
                     'name' : 'Training graph'
                    })
     draw_graphs([graphFile])