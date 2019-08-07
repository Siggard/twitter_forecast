import tweepy
import os
import glob
import sqlite3
import time

consumer_key = 'gijaNPO1RVGy2lKkCUxUw'
consumer_secret = 'gWCy6OIpHYGhSMrj0D5pjOmnJQP55M7BF0X35T6XMQ'
access_token = '363931816-LGB5m13W9oxdj8ktG3eBw1box4W0YBLqI4FP8PkL'
access_token_secret = 'zgBBsmYczXncka89ONP7LfyeZbdl7cYeE4cRGEh5TeA'
path_to_dir = 'clubs'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

con = sqlite3.connect('bas_twitts.db')
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS account_data(Account TEXT, DateLastParse TEXT, DataFromEpoch FLOAT)')
con.commit()


def twitts_user(user_name, count_twitts=1):
    user = api.get_user(user_name)
    public_tweets = api.user_timeline(user_name, count=count_twitts)
    for tweet in public_tweets:
        print(tweet.text)


os.chdir(path_to_dir)
for file in glob.glob("*.txt"):
    # print("\nFile: " + file + "\n")
    file_open = open(file)
    for line in file_open:
        name_line = line
        name_short = name_line.split('/')
        name_short = name_short[-1]
        time_epoch = time.time()
        full_time_name = time.ctime(time.time())
        count = [name_short, full_time_name, time_epoch]
        cur.execute('INSERT INTO account_data VALUES(?, ?, ?)', count)
        con.commit()
        twitts_user(name_short)
