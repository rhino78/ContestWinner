__author__ = 'ryan.shave'
import tweepy
import tweet_creds_contest
import sqlite3
import sys
import logging

def log(error_msg):
    logging.basicConfig(filename='contest_tweet.log', level=logging.INFO)
    logging.info('Tweet log error message: ' + error_msg)

auth = tweepy.OAuthHandler(tweet_creds_contest.CONSUMER_KEY, tweet_creds_contest.CONSUMER_SECRET)
auth.set_access_token(tweet_creds_contest.ACCESS_KEY, tweet_creds_contest.ACCESS_SECRET)
api = tweepy.API(auth)

query = '"RT to win"'
max_tweets = 20


try:
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]
except tweepy.TweepError as e:
    log(e.response)


for t in searched_tweets:
    api.retweet(t.id)
    api.create_friendship(t.user.id)
    tweet = t.text.encode(sys.stdout.encoding, errors='replace')
    conn = sqlite3.connect(r"C:\python34\contest.db")
    cursor = conn.cursor()
    cursor.execute('insert into contest_data(tweet_text, tweet_date) values(?, CURRENT_TIMESTAMP)', (tweet,))
    conn.commit()
    cursor.execute('insert into following(twitterid, date) values(?, CURRENT_TIMESTAMP)', (t.id,))
    conn.commit()
    conn.close()
