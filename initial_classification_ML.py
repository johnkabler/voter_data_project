import numpy as np
import pandas as pd
tweets_party = pd.read_csv('data/makindo_data.csv')


# from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(tweets_party.tweet)
#Random Forest requires a non-sparse matrix
X = X.toarray()
# X = np.asarray(tweets_party.tweet, dtype="|S6")
targets = np.asarray(tweets_party.party_affiliation, dtype="|S6")

#Data is ready and vectorized.  Let's pull in random forest and use it for
#classification
from sklearn.ensemble import RandomForestClassifier

classifier = RandomForestClassifier(n_estimators=20)
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
