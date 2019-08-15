import tweepy
import sqlite3
from os import chdir
from glob import glob
from pathlib import Path
from time import sleep, ctime


consumer_key = 'gijaNPO1RVGy2lKkCUxUw'
consumer_secret = 'gWCy6OIpHYGhSMrj0D5pjOmnJQP55M7BF0X35T6XMQ'
access_token = '363931816-LGB5m13W9oxdj8ktG3eBw1box4W0YBLqI4FP8PkL'
access_token_secret = 'zgBBsmYczXncka89ONP7LfyeZbdl7cYeE4cRGEh5TeA'
path_to_dir = 'clubs'
db_name = 'db_twitts.db'
positivfile = 'positive.txt'
negativfile = 'negative.txt'
count_twitts = 20

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

con = sqlite3.connect(db_name)
cur = con.cursor()


def check_for_duplication(user_name, idt):
    recuestdb = 'SELECT IdTwett FROM ' + user_name
    cur.execute(recuestdb)
    data_column = cur.fetchall()
    new_data = []
    for element in data_column:
        new_data.append(element[0])
    data_column = new_data
    del(new_data)
    for i in data_column:
        if i == idt:
            return True


def positiv_words(user_name, texttwiit):
    text_twit_list = texttwiit.split()
    p = Path(__file__).parents[0]
    open_positive_words = open(str(p) + '\\' + positivfile, 'r')
    positiv_word_list = list(map(lambda x:x.strip(),open_positive_words))
    for i in positiv_word_list:
        for ii in text_twit_list:
            if i == ii:
                return True


def negativ_words(user_name, texttwiit):
    text_twit_list = texttwiit.split()
    p = Path(__file__).parents[0]
    open_negativ_words = open(str(p) + '\\' + negativfile, 'r')
    negativ_word_list = list(map(lambda x: x.strip(), open_negativ_words))
    for i in negativ_word_list:
        for ii in text_twit_list:
            if i == ii:
                return True


def twitts_user(user_name, count_twitts):
    public_tweets = api.user_timeline(user_name, count=count_twitts)
    for tweet in public_tweets:
        timetwitt = tweet.created_at
        idt = tweet.id
        texttwiit = tweet.text
        if check_for_duplication(user_name, idt) == True:
            continue
        elif positiv_words(user_name, texttwiit) == True:
            NegativWords = ""
            PositivWords = "1"
            caunt_positiv = [timetwitt, idt, PositivWords, NegativWords, texttwiit]
            cur.execute('INSERT INTO %s VALUES(?, ?, ?, ?, ?)' % name_short, caunt_positiv)
            con.commit()
        elif negativ_words(user_name, texttwiit) == True:
            NegativWords = "1"
            PositivWords = ""
            caunt_negativ = [timetwitt, idt, PositivWords, NegativWords, texttwiit]
            cur.execute('INSERT INTO %s VALUES(?, ?, ?, ?, ?)' % name_short, caunt_negativ)
            con.commit()
        else:
            continue


while True:
    cur.execute('CREATE TABLE IF NOT EXISTS DataParsing(UpdataTime TEXT)')
    updata_time = ctime()
    cur.execute('INSERT INTO DataParsing VALUES(?)', (updata_time,))
    con.commit()
    chdir(path_to_dir)
    for file in glob("*.txt"):
        file_open = open(file)
        for line in file_open:
            name_short = line.split('/')
            name_short = name_short[-1]
            cur.execute('CREATE TABLE IF NOT EXISTS %s'
                        '(TimeTwitt TEXT, IdTwett INTEGER, '
                        'PositivWords TEXT, NegativWords TEXT, '
                        'TextTwitt TEXT)' % name_short)
            twitts_user(name_short, count_twitts)
    p = Path(__file__).parents[0]
    chdir(p)
    sleep(3600)#falls asleep for 60 minutes and repeats the cycle