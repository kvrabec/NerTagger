import data
import nltk
import os

classification_data_folder = 'classificationData/'
taggedArticleFile = classification_data_folder + 'taggedArticles.tag'

def process_article(ner_article):
    processed_article = []
    for line in ner_article:
        if type(line) == nltk.Tree:
            label = line._label
            words_and_pos = []
            if line._label == 'PERSON':
                for index, word in enumerate(line):
                    if index == 0:
                        processed_article.append('/'.join(word) + '/B-' + label)
                    else:
                        processed_article.append('/'.join(word) + '/I-' + label)
            else:
                for index, word in enumerate(line):
                        processed_article.append('/'.join(word))                            
        else:
            processed_article.append('/'.join(line))
    return processed_article

processed_articles_array = []

file_open_mode = 'w'

if os.path.exists(taggedArticleFile) and os.path.isfile(taggedArticleFile):
    file_open_mode = 'r'

with open(taggedArticleFile, file_open_mode, encoding='utf-8') as f:
    if file_open_mode == 'r':
        processed_articles_array = f.readlines()
    else:
        articles = data.getAllArticles()
        for article in articles:
            article_text = article['text']
            tokenized_article = nltk.tokenize.word_tokenize(article_text)
            pos_tagged_article = nltk.pos_tag(tokenized_article)
            ner_tagged_article = nltk.ne_chunk(pos_tagged_article)
            processed_article = process_article(ner_tagged_article)
            for line in processed_article:
                f.write(line + '\n')
            processed_articles_array.extend(processed_article)

