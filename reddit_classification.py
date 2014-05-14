import pandas as pd
import numpy as np

# vectorizer = StemmedCountVectorizer(min_df=1, stop_words='english', ngram_range=(1,2))
# from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfTransformer

comments = pd.read_pickle('data/comment_corpus.pickle')
comments.columns = ['comment', 'party_affiliation', 'category']

political = comments.category == 'POLITICAL'

def encoder(string_of_text):
    return string_of_text.encode('utf-8').strip()

comments['encoded_comment'] = comments.comment.apply(encoder)

X = np.asarray(comments['encoded_comment'].copy(), dtype='|S6')

Y = np.asarray(comments.category.copy(), dtype='|S6')

from sklearn.feature_extraction.text import CountVectorizer

import nltk.stem
english_stemmer = nltk.stem.SnowballStemmer('english')
class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))


pipeline = Pipeline([
                     ('vectorizer', StemmedCountVectorizer()),
                     ('tfidf_transformer',  TfidfTransformer()),
                     ('classifier', MultinomialNB())
                     ])

pipeline.set_params(vectorizer__min_df=1, vectorizer__stop_words='english')


from sklearn.cross_validation import KFold


k_fold = KFold(n=len(X), n_folds=3, indices=False)
scores = []


for train_indices, test_indices in k_fold:
    train_text = X[train_indices]
    train_y = Y[train_indices]

    test_text = X[test_indices]
    test_y = Y[test_indices]

    pipeline.fit(train_text, train_y)
    score = pipeline.score(test_text, test_y)
    scores.append(score)

score = sum(scores) / len(scores)
print(score)
