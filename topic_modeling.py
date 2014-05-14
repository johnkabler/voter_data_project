from declass.utils import gensim_helpers
from gensim import models, similarities, corpora
import pandas as pd
import numpy as np
import gensim

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import nltk.stem
import string

voters = pd.read_csv('data/pulled_tweets_cleaned.csv')

# poli_tweets = pd.read_csv('data/navy/keyword-tweets.txt', sep='\t', header=None)
# poli_tweets.columns = ['political', 'tweet']
# political = poli_tweets.political == 'POLIT'
poli_comments = pd.read_pickle('data/reddit_poli_comments.pickle')


stop = stopwords.words('english')
for i in list(string.punctuation):
    stop.append(i)


def df_tokenizer(text):
    token_list = []
    for sent in sent_tokenize(text):
        for word in word_tokenize(sent.lower()):
            if word not in stop:
                token_list.append(word)
    return token_list

poli_comments['tokens'] = poli_comments.comment.apply(df_tokenizer)
voters['tokens'] = voters.tweet.apply(df_tokenizer)

dictionary = gensim.corpora.Dictionary(poli_comments.tokens)
dictionary.filter_extremes()
dictionary.save('topic_dict.dict')

corpus = [dictionary.doc2bow(text) for text in voters.tokens]
corpora.MmCorpus.serialize('data/corpus.mm', corpus)

model = models.ldamodel.LdaModel(corpus, num_topics=50, id2word=dictionary)

topics_df = gensim_helpers.get_topics_df(corpus, model)
voters_topics = pd.concat([voters, topics_df], axis=1)

voters_topics.to_pickle('data/voters_topics_50.pickle')
