import praw
import time
import pandas as pd

## Comment out the new list declaration.  I'll run this once every hour or so to build up a corpus of text with political labels
#comments_list = []

r = praw.Reddit('Comment parser example by u/johnkabler')
poli_subreddit_list = ['politics', 'Conservative', 'Republican', 'Progressive', 'Libertarian', 'teaparty', 'liberal','christian']

#First let's get our political comments corpus of 175 comments from various politically oriented sections of the
#link aggregation and discussion website Reddit.com

for i in poli_subreddit_list:
    political_subreddit = r.get_subreddit(i)
    poli_comments = r.get_comments(political_subreddit)

    for comment in poli_comments:
        comment_item = {}
        comment_item['comment'] = comment.body
        comment_item['type'] = 'POLITICAL'

        if (i == 'politics')|(i == 'Progressive')|(i == 'liberal'):
            comment_item['partisan_affiliation'] = 'DEM'
        else:
            comment_item['partisan_affiliation'] = 'REP'
        comments_list.append(comment_item)

non_poli_subreddit_list = ['fitness', 'funny', 'pics', 'sports', 'todayilearned', 'music', 'movies','nba', 'collegebasketball']

for i in non_poli_subreddit_list:
    non_poli_subreddit = r.get_subreddit(i)
    non_poli_comments = r.get_comments(non_poli_subreddit)

    for comment in non_poli_comments:
        comment_item = {}
        comment_item['comment'] = comment.body
        comment_item['type'] = 'NOT'
        comment_item['partisan_affiliation'] = 'NA'
        comments_list.append(comment_item)

comment_corpus = pd.DataFrame(comments_list)

comment_corpus = comment_corpus.drop_duplicates()

political = comment_corpus.type == 'POLITICAL'
political_comments = comment_corpus[political]

political_comments.to_pickle('data/reddit_poli_comments.pickle')

#Let's also write out our raw comments corpus so we can try to write a political
#comment filter.  
