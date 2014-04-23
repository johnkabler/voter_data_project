import numpy as np
import pandas as pd
tweets_party = pd.read_csv('data/pulled_tweets.csv')


from sklearn.feature_extraction.text import CountVectorizer



# #### Let's build a better vectorizer by extending the CountVectorizer function and overwriting the "build_analyzer" function with a customized stemmer pulled in from nltk
import nltk.stem
english_stemmer = nltk.stem.SnowballStemmer('english')
class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))

vectorizer = StemmedCountVectorizer(min_df=1, stop_words='english')

counts = vectorizer.fit_transform(tweets_party.tweet)


from sklearn.naive_bayes import MultinomialNB

classifier = MultinomialNB()

targets = np.asarray(tweets_party.party_affiliation, dtype="|S6")

classifier.fit(counts,targets)


examples = ['I love Jesus, lets go hunting!', 'Legalize marijuana now! Peace and love']


example_counts = vectorizer.transform(examples)


predictions = classifier.predict(example_counts)

print(predictions)

# array(['REP', 'DEM'],
      # dtype='|S3')

#Initial success, but needs work.  Still uses bag of words,
#which won't stand up to real complexity.  Possibly need to
#incorporate sentiment analysis.

#Let's use pipeline to clean up the testing process

from sklearn.pipeline import Pipeline

#Bernoulli is often more appropriate for tweets and other short messages
from sklearn.naive_bayes import BernoulliNB


pipeline = Pipeline([
                     ('vectorizer', StemmedCountVectorizer(min_df=1, stop_words='english')),
#                      ('tfidf_transformer',  TfidfTransformer()),
                     ('classifier', BernoulliNB(binarize=0.0))
                     ])


pipeline.fit(np.asarray(tweets_party.tweet), targets)


pipeline.predict(examples)


# ## Cross Validation Time

from sklearn.cross_validation import KFold


k_fold = KFold(n=len(tweets_party), n_folds=6, indices=False)
scores = []


for train_indices, test_indices in k_fold:
    train_text = np.asarray(tweets_party[train_indices]['tweet'])
    train_y = np.asarray(tweets_party[train_indices]['party_affiliation'], dtype="|S6")

    test_text = np.asarray(tweets_party[test_indices]['tweet'])
    test_y = np.asarray(tweets_party[test_indices]['party_affiliation'], dtype="|S6")

    pipeline.fit(train_text, train_y)
    score = pipeline.score(test_text, test_y)
    scores.append(score)
    
score = sum(scores) / len(scores)
print(score)
