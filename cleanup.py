import tweepy
import tweet_creds_contest
auth = tweepy.OAuthHandler(tweet_creds_contest.CONSUMER_KEY, tweet_creds_contest.CONSUMER_SECRET)
auth.set_access_token(tweet_creds_contest.ACCESS_KEY, tweet_creds_contest.ACCESS_SECRET)
api = tweepy.API(auth)
ids = []

for p in tweepy.Cursor(api.friends_ids, screen_name="PythonDork").pages():
	ids.extend(p)

for d in ids:
	api.destroy_friendship(d)
	print("killed it: {0}".format(d))
