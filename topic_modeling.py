from gensim import models, similarities, corpora
import pandas as pd
import numpy as np
import gensim

from nltk.tokenize import word_tokenize, sent_tokenize
import nltk.stem

voters = pd.read_csv('data/pulled_tweets_cleaned.csv')

def df_tokenizer(text):
    token_list = []
    for sent in sent_tokenize(text):
        for word in word_tokenize(sent):
            token_list.append(word.lower())
    return token_list

voters['tokens'] = voters.tweet.apply(df_tokenizer)

dictionary = gensim.corpora.Dictionary(voters.tokens)
dictionary.save('topic_dict.dict')

corpus = [dictionary.doc2bow(text) for text in voters.tokens]
corpora.MmCorpus.serialize('data/corpus.mm', corpus)

model = models.ldamodel.LdaModel(corpus, num_topics=100, id2word=dictionary)
