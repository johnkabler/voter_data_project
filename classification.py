import pandas as pd
import numpy as np

voters_lda = pd.read_pickle('data/voters_topics_sentiment.pickle')

X = voters_lda.copy()

voters_lda['is_rep'] = (voters_lda.party_affiliation == 'REP').astype(int)
voters_lda['is_dem'] = (voters_lda.party_affiliation == 'DEM').astype(int)
voters_lda['is_npa'] = (voters_lda.party_affiliation == 'NPA').astype(int)



target = voters_lda.copy()


del X['party_affiliation']
del X['tweet']


# target = np.asarray(target.party_affiliation, dtype='|S6')
target = target.is_dem

from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestClassifier

from sklearn.naive_bayes import MultinomialNB

classifier = MultinomialNB()

from sklearn.cross_validation import KFold


k_fold = KFold(n=len(X), n_folds=6, indices=False)
scores = []


for train_indices, test_indices in k_fold:
    train_text = X[train_indices]
    train_y = target[train_indices]

    test_text = X[test_indices]
    test_y = target[test_indices]

    classifier.fit(train_text, train_y)
    score = classifier.score(test_text, test_y)
    scores.append(score)

score = sum(scores) / len(scores)
print(score)

##Results aren't good enough.  The likely culprit is that I'm trying
##to classify partisan affiliation of non-political tweets.

##Next step is to use a political and non-political comment corpus to train
##and test a naive bayes classifier to detect filter non-political text.

# This way only political text is attempted for classification.
