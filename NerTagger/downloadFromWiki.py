import tqdm
import re
import urllib
import os
import pandas as pd
import unicodedata
from bs4 import BeautifulSoup
from pymongo import MongoClient
from prepareEmbeddings import SentenceGetter
import nltk
from pycorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('http://localhost:9000')
def start_StanfordCoreNLP_server():
    os.system('start cmd /k java -mx4g -cp "stanford-corenlp-full-2018-10-05/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 30000')

start_StanfordCoreNLP_server()

def downloadDataFromWiki(link):
    wikiUrl = link
    html = urllib.request.urlopen(wikiUrl).read()
    soup = BeautifulSoup(html,"html5lib")
    alltext = ""
    paragraphs = soup.findAll('p')
    for paragraph in tqdm.tqdm(paragraphs,
                                    total=len(paragraphs),
                                    unit_scale=True, unit=" paragraphs",
                                    desc="Parsing paragraphs"):
            text = ''.join(paragraph.findAll(text = True))
            if text.isspace() or text == '':
                    continue
            text = re.sub(r"\[.*?\]","", text.strip())
            if(alltext == ""):
                    text = re.sub(r" \([^\)]*\)","", text)
            alltext += text + " "

    return alltext

def addToDataset(link, dataset_path):
    columns = ['Sentence #','Word', 'POS','Tag']
    alltext = downloadDataFromWiki(link)
    alltext = unicodedata.normalize('NFKD', alltext)
    sentences_output = nlp.annotate(alltext, properties={
        'annotators': 'tokenize,ssplit,pos,ner',
        'outputFormat': 'json'}
    )
    dataset = pd.read_csv(dataset_path, encoding="latin1")
    dataset_sentences = SentenceGetter(dataset)
    start_index = len(dataset_sentences.sentences)
    for sentence in sentences_output:
        for index, pair in enumerate(tagged_words):
            if index == 0:
                dataset = dataset.append(
                    pd.Series(['Sentence: ' + str(index + start_index),pair[0],pair[1],None], index=[ 'Sentence #','Word', 'POS','Tag' ]), ignore_index = True)
            else:
                dataset = dataset.append(
                    pd.Series([None,pair[0],pair[1],None], index=columns), ignore_index = True)
    pd.DataFrame(data=dataset).to_csv('embeddingData_b\\ner_dataset_1.csv', columns=columns,index=False)

addToDataset('https://en.wikipedia.org/wiki/Luka_Modri%C4%87', os.path.dirname(os.path.abspath(__file__)) + '\\embeddingData_b\\ner_dataset.csv')
