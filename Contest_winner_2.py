__author__ = 'ryan.shave'
import tweepy
import tweet_creds_contest
import sqlite3
import sys
import logging

def not_in_db(status):
        conn = sqlite3.connect(r"C:\Python34\contest.db")
        cursor = conn.cursor()
        cursor.execute('select 1 from contest_data where tweet_text = ?', (status,))
        if cursor.fetchone():
                return False
        else:
                return True

auth = tweepy.OAuthHandler(tweet_creds_contest.CONSUMER_KEY, tweet_creds_contest.CONSUMER_SECRET)
auth.set_access_token(tweet_creds_contest.ACCESS_KEY, tweet_creds_contest.ACCESS_SECRET)
api = tweepy.API(auth)

query = '"rt to win"'
max_tweets = 100
success = 0
fail = 0
duplicates = 0
conn = sqlite3.connect(r"C:\python34\contest.db")
cursor = conn.cursor()

searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]

logging.basicConfig(filename='contest_tweet.log', level=logging.INFO)
logging.info("Attempting to RT {0} tweets".format(len(searched_tweets)))
searched_tweets.reverse()

for t in searched_tweets:
    tweet = t.text.encode(sys.stdout.encoding, errors='replace')
    
    #check in the DB first
    if not_in_db(tweet):
        try:
            api.retweet(t.id)
            api.create_friendship(t.user.id)
            success += 1
            cursor.execute('insert into contest_data(tweet_text, tweet_date, tweet_id) values({0}, CURRENT_TIMESTAMP, {1})'.format(tweet,t.id))
            conn.commit()
            cursor.execute('insert into following(twitterid, date) values(?, CURRENT_TIMESTAMP)', (t.user.id,))
            conn.commit()
        except tweepy.TweepError as e:
            fail +=1
            #log it anyway
            cursor.execute('insert into contest_data(tweet_text, tweet_date, tweet_id) values({0}, CURRENT_TIMESTAMP, {1})'.format(tweet,t.id))
            conn.commit()
            logging.info("could not tweet {0}".format(tweet))
            logging.info("reason response: {0}".format(e))
    else:
        duplicates +=1  




logging.info(" successfull tweets: {0} | fails: {1} | duplicates {2}.".format(success, fail, duplicates))
conn.close()
