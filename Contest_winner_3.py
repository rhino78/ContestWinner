__author__ = 'ryan.shave'
import tweepy
import tweet_creds_contest
import sqlite3
import sys
import logging
import time
import useful_functions
from datetime import date
import calendar

my_date = date.today()
day = calendar.day_name[my_date.weekday()]
if day == 'Friday':
        querystr = '"RT to win" #FreebieFriday'
elif day == 'Wednesday':
        querystr = '"RT to win"  #WinItWednesday'
elif day == 'Tuesday':
        querystr = '"RT to #WIN"'
else:
        querystr = '"RT to win"'


max_tweets = 175
success = 0
fail = 0
duplicates = 0
cunts = 0
banned_ids = useful_functions.banned_ids()

auth = tweepy.OAuthHandler(tweet_creds_contest.CONSUMER_KEY, tweet_creds_contest.CONSUMER_SECRET)
print(auth)
auth.set_access_token(tweet_creds_contest.ACCESS_KEY, tweet_creds_contest.ACCESS_SECRET)
api = tweepy.API(auth)
print(api)
searched_tweets = [status for status in tweepy.Cursor(api.search, q=querystr).items(max_tweets)]

logging.basicConfig(filename='contest_tweet.log', level=logging.INFO)
logging.info("Attempting to RT {0} tweets with a query of {1}".format(len(searched_tweets), querystr))
searched_tweets.reverse()

for t in searched_tweets:
        tweet = t.text.encode(sys.stdout.encoding, errors='replace')
        if hasattr(t, 'retweeted_status'):
                orig_id = t.retweeted_status.id_str
                user_id = t.retweeted_status.user.id_str
                print('rt status')
        elif not str(t.in_reply_to_user_id):
                print('reply status')
                orig_id = t.in_reply_to_status_id_str
                user_id = t.in_reply_to_user_id_str
        else:
                print('plain status')
                orig_id = t.id_str
                user_id = t.user.id_str

        if user_id in banned_ids:
                cunts +=1
        elif not orig_id:
                logging.info("got a null id {0}".format(t.id_str))
        elif useful_functions.id_not_in_db(orig_id):
                try:
                        api.retweet(orig_id)
                        api.create_friendship(user_id)
                        success += 1
                        useful_functions.log_in_db(tweet, orig_id, user_id)
                except tweepy.TweepError as e:
                        fail +=1
                        useful_functions.log_in_db(tweet, orig_id, user_id)
                        logging.info("could not tweet {0} id: {1}".format(tweet, orig_id))
                        logging.info("reason response: {0}".format(e))
                        logging.info(e)
                        if e.args[0][0]['code'] == 136:
                                useful_functions.ban(orig_id)
                                logging.info("banned")
                                print(e)
        else:
                duplicates +=1




logging.info(" successfull tweets: {0} | fails: {1} | duplicates {2} | cunts {3}.".format(success, fail, duplicates, cunts))
if success == 0:
        api.update_status(status="I just entered in {0} contests :( \n {1}".format(success, time.strftime("%m/%d/%Y")))
elif success > 29:
        api.update_status(status="I just entered in {0} contests! YIPPIE! \n {1}".format(success, time.strftime("%m/%d/%Y")))
else:
        api.update_status(status="I just entered in {0} contests! \n {1}".format(success, time.strftime("%m/%d/%Y")))
