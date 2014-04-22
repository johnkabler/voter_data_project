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
