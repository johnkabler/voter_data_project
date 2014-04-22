# ## Get the training data from Twitter
#
# * First, we need to set up the Twitter API info and make sure its working
# * Next, we need to fetch a single user's tweets to analyze the structure and figure out how to get the text out
# * Finally, for each user in our list of users with matched voter records, we need to pull in all of their tweets for training data

from twitter import *
import time

from auth_twitter import access_token, access_token_secret,
                         consumer_key, consumer_secret

t = Twitter(auth=OAuth(access_token, access_token_secret, consumer_key, consumer_secret))

import numpy as np
import pandas as pd
import datetime
import dateutil


def get_age(birth_date):
    # Get the current date
    now = datetime.datetime.utcnow()
    now = now.date()

    # Get the difference between the current date and the birthday
    age = dateutil.relativedelta.relativedelta(now, birth_date)
    age = age.years

    return age


vote_raw = pd.read_csv('data/makindo_data.csv', parse_dates=['birth_date'])

vote_raw['age'] = vote_raw.apply(lambda row: get_age(row['birth_date']), axis = 1)


vote_clean = vote_raw[['twitter_handle', 'party_affiliation', 'age']].copy()

# Helper function to fetch each matched user's tweets.  This will
# increase corpus size by a factor of 20.

# One catch:  Twitter API hates this, so i have to wait a few seconds
# between each call or I'll get blacklisted
def get_tweets(username):
    try:
        user_status = t.statuses.user_timeline(screen_name=username)
        time.sleep(12)
        return [x['text'] for x in user_status]
    except:
        return ''


tweets_list = [{row[1][1]:get_tweets(row[1][0])} for row in vote_clean.iterrows()]
# More to come.  Next step is to spit this out into CSV for crunching in
# scikit.  My bet is that Naive Bayesian will work best for predictions.
party_tweet_list = []
for user in tweets_list:
    for key in user:
        for tweet in user[key]:
            item = [tweet, key]
            party_tweet_list.append(item)

# Write out the returned list object to a pandas dataframe, then
# convert and write to csv.

full_tweets = pd.DataFrame(party_tweet_list, columns=['tweet', 'party_affiliation'])
full_tweets.to_csv('data/pulled_tweets.csv', encoding='utf8')

#This is now 18,000 plus Tweets with a party affiliation of the writer
#attached.  Should be a great corpus for Naive Bayesian analysis
#after N-gram vectorization.  
