import numpy as np
import pandas as pd
tweets_party = pd.read_csv('data/pulled_tweets_republican.csv')


from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.feature_extraction.text import TfidfVectorizer

import nltk.stem
english_stemmer = nltk.stem.SnowballStemmer('english')
class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))

vectorizer = StemmedCountVectorizer(min_df=.1, stop_words='english',decode_error='ignore',
                              ngram_range=(1,5))

X = vectorizer.fit_transform(np.asarray(tweets_party.tweet, dtype="|S6"))
#Random Forest requires a non-sparse matrix
# X = X.toarray()
# X = np.asarray(tweets_party.tweet, dtype="|S6")
# targets = np.asarray(tweets_party.party_affiliation, dtype="|S6")
targets = np.asarray(tweets_party.is_republican)
from sklearn.naive_bayes import MultinomialNB
# from sklearn.svm import LinearSVC
# classifier = LinearSVC()
classifier = MultinomialNB()
# ## Cross Validation Time

from sklearn.cross_validation import KFold


k_fold = KFold(n=len(tweets_party), n_folds=6, indices=False)
scores = []


for train_indices, test_indices in k_fold:
    train_text = X[train_indices]
    train_y = targets[train_indices]

    test_text = X[test_indices]
    test_y = targets[test_indices]

    classifier.fit(train_text, train_y)
    score = classifier.score(test_text, test_y)
    scores.append(score)

score = sum(scores) / len(scores)
print(score)

# Test failed.  Random Forest didn't bring any improvement.  Need to use the
# newly acquired sentiment corpus to train and then add a sentiment feature.

# Also need to cleanse my newly acquired partisan tweets of emoticons to prevent
# Numpy errors.
