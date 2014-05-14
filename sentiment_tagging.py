import pandas as pd

sent_file = pd.read_csv('data/sentiment_analysis/AFINN-111.txt', header=None, sep='\t', names=['word', 'score'], index_col='word')

sent_dict = sent_file.T.to_dict()

#many classifiers can't handle negative numbers.   We'll have to take sentiment and bucket it into 1 for negativee, 2 for neutral,
#or 3 for positive
def find_sentiment(tweet):
    score = 0.0
    for word in tweet.lower().split():
        if word in sent_dict:
            score += float(sent_dict[word]['score'])
    if score < 0:
        return 1
    elif score > 0:
        return 3
    else:
        return 2

makindo_tokens = pd.read_csv('data/pulled_tweets_cleaned.csv')
makindo_tokens['sentiment'] = makindo_tokens.tweet.apply(find_sentiment)

voters_topics = pd.read_pickle('data/voters_topics_50.pickle')

# Clean up the unneeded columns

del voters_topics['Unnamed: 0']
del voters_topics['tokens']

del makindo_tokens['Unnamed: 0']
del makindo_tokens['party_affiliation']
del makindo_tokens['tweet']

# merge into a single dataframe

voters_topics_sentiment = pd.concat([makindo_tokens, voters_topics], axis=1)

#pickle the data for use in the classifier
voters_topics_sentiment.to_pickle('data/voters_topics_sentiment.pickle')
