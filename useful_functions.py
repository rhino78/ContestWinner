import tweepy
import tweet_creds_contest
import sqlite3

auth = tweepy.OAuthHandler(tweet_creds_contest.CONSUMER_KEY, tweet_creds_contest.CONSUMER_SECRET)
auth.set_access_token(tweet_creds_contest.ACCESS_KEY, tweet_creds_contest.ACCESS_SECRET)
api = tweepy.API(auth)

#limits = api.rate_limit_status()
#remain_search_limits = limits['resources']['search']['/search/tweets']['remaining']
#remain_search_limits

def user_id_by_tweet(id):
    tweet = api.get_status(id)
    return tweet.user.id_str

def not_in_db(status):
        conn = sqlite3.connect(r"C:\Python34\contest.db")
        cursor = conn.cursor()
        cursor.execute('select 1 from contest_data where tweet_text = ?', (status,))
        if cursor.fetchone():
                return False
        else:
                return True

def log_in_db(tweet,orig_id, user_id):
    conn = sqlite3.connect(r"C:\python34\contest.db")
    cursor = conn.cursor()
    cursor.execute('insert into contest_data(tweet_text, tweet_date, tweet_id) values(?, CURRENT_TIMESTAMP, ?)', (tweet,orig_id))
    conn.commit()
    cursor.execute('insert into following(twitterid, date) values(?, CURRENT_TIMESTAMP)', (user_id,))
    conn.commit()


def get_user_by_id(id):
    u = api.get_user(id)
    return u.screen_name

def get_user_by_screen_name(name):
    user = api.get_user(screen_name = name)
    return user.id_str

def banned_ids():
    bids = []
    conn = sqlite3.connect(r"C:\python34\contest.db")
    cursor = conn.cursor()
    cursor.execute("select id from banned")
    row = cursor.fetchone()
    for row in cursor:
        bids.extend(row)

    return bids
    

def id_not_in_db(id):
        conn = sqlite3.connect(r"C:\Python34\contest.db")
        cursor = conn.cursor()
        cursor.execute('select 1 from contest_data where tweet_id = ?', (id,))
        if cursor.fetchone():
                return False
        else:
                return True

def ban(id):
    ban_id = user_id_by_tweet(id)
    conn = sqlite3.connect(r"C:\Python34\contest.db")
    cursor = conn.cursor()
    cursor.execute('insert into banned(id) values({0})'.format(ban_id))
    conn.commit()
