import pandas as pd

sent_file = pd.read_csv('data/sentiment_analysis/AFINN-111.txt', header=None, sep='\t', names=['word', 'score'], index_col='word')

sent_dict = sent_file.T.to_dict()

def find_sentiment(tweet):
    score = 0.0
    for word in tweet.lower().split():
        if word in sent_dict:
            score += float(sent_dict[word]['score'])
    if score > 0:
        return 'POS'
    elif score < 0:
        return 'NEG'
    else:
        return 'NA'

makindo_tokens = pd.read_csv('data/makindo_tokenized.csv')
makindo_tokens['sentiment'] = makindo_tokens.tweet.apply(find_sentiment)

makindo_tokens.to_csv('data/sentiment_analysis/makindo_sentiment.csv')
