import tweepy
import sqlite3
import time
import datetime
from os import chdir
from glob import glob
from pathlib import Path
from re import findall

consumer_key = 'gijaNPO1RVGy2lKkCUxUw'
consumer_secret = 'gWCy6OIpHYGhSMrj0D5pjOmnJQP55M7BF0X35T6XMQ'
access_token = '363931816-LGB5m13W9oxdj8ktG3eBw1box4W0YBLqI4FP8PkL'
access_token_secret = 'zgBBsmYczXncka89ONP7LfyeZbdl7cYeE4cRGEh5TeA'
path_to_dir = 'clubs'
db_name = 'db_twitts.db'
positivfile = 'positive.txt'
negativfile = 'negative.txt'
count_twitts = 4

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

con = sqlite3.connect(db_name)
cur = con.cursor()
print('Started working and connected to the database: ', db_name)


# function of checking twitts in the table football club
def check_for_duplication(user_name, club_names, idt):
    recuestdb = 'SELECT alias, idtwitt FROM ' + club_names
    cur.execute(recuestdb)
    data_column = cur.fetchall()
    for i in range(0, len(data_column)):
        c = 0
        a = data_column[i][c]
        if a == user_name:
            c = 1
            b = data_column[i][c]
            if b == idt:
                return True


# function search positive word in twitt
def positiv_words(user_name, club_names, texttwiit):
    p = Path(__file__).parents[0]
    open_positive_words = open(str(p) + '\\' + positivfile, 'r')
    positiv_word_list = list(map(lambda x: x.strip(), open_positive_words))
    for i in positiv_word_list:
        res = findall(i, texttwiit)
        if ''.join(res) != '':
            return True


# function search negative word in twitt
def negativ_words(user_name, club_names, texttwiit):
    p = Path(__file__).parents[0]
    open_negativ_words = open(str(p) + '\\' + negativfile, 'r')
    negativ_word_list = list(map(lambda x: x.strip(), open_negativ_words))
    for i in negativ_word_list:
        res = findall(i, texttwiit)
        if ''.join(res) != '':
            return True


# The main function of checking the user's tweets for positive and negative words
def brain_bot(user_name, club_names, count_twitts):
    public_tweets = api.user_timeline(user_name, count=count_twitts)
    print('Get the', count_twitts, 'latest tweets user: ', user_name)
    for tweet in public_tweets:
        timetwitt = tweet.created_at
        idt = tweet.id
        texttwiit = tweet.text
        if check_for_duplication(user_name, club_names, idt) == True:
            continue
        elif positiv_words(user_name, club_names, texttwiit) == True:
            NegativWords = 0
            PositivWords = 1
            last_parse_day = datetime.datetime.today().strftime("%d%m%Y")
            caunt_positiv = [user_name, club_names, timetwitt, PositivWords, NegativWords, idt, last_parse_day]
            cur.execute('INSERT INTO %s VALUES(?, ?, ?, ?, ?, ?, ?)' % club_names, caunt_positiv)
            con.commit()
            print('MADE A POSITIVE TWITT in the table of the club: ', club_names)
        elif negativ_words(user_name, club_names, texttwiit) == True:
            NegativWords = 1
            PositivWords = 0
            last_parse_day = datetime.datetime.today().strftime("%d%m%Y")
            caunt_positiv = [user_name, club_names, timetwitt, PositivWords, NegativWords, idt, last_parse_day]
            cur.execute('INSERT INTO %s VALUES(?, ?, ?, ?, ?, ?, ?)' % club_names, caunt_positiv)
            con.commit()
            print('MADE A NEGATIVE TWITT in the table of the club: ', club_names)
        else:
            continue


# Create total a table with columns:
cur.execute('CREATE TABLE IF NOT EXISTS Total_Table('
            'alias TEXT, '  # alias - name of the twitter user
            'club_alias TEXT, '  # club_alias - belonging to a football club
            'lastparse INTEGER)'  # lastparse - recent processing time from the beginning of the era
            )
print('Connected to table Total_Table. Columns: alias TEXT, club_alias TEXT, lastparse INTEGER')
chdir(path_to_dir)
print('Opened folder: ', path_to_dir)
for file in glob("*.txt"):
    print('Find file: ', file)
    club_names = file.split('.txt')
    club_names = club_names[0]
    # Create a football club table with columns:
    cur.execute('CREATE TABLE IF NOT EXISTS %s('
                'alias TEXT, '  # alias - name of the twitter user
                'club_alias TEXT, '  # club_alias - belonging to a football club
                'time_twitt INTEGER, '  # time_twitt - date of publication of the tweet
                'positive INTEGER, '  # positive - a sign that the news is positive
                'negative INTEGER, '  # negative - a sign that the news is negative
                'idtwitt INTEGER, '  # idtwiit - tweet identification number
                'lastparseday INTEGER)'  # lastparseday - day of adding to the database
                % club_names)
    print('Connected to table football club: ', club_names)
    file_open = open(file)
    print('Opened file: ', file)
    for line in file_open:
        name_short = line.split('/')
        name_short = list(map(lambda x: x.strip(), name_short))
        name_short = name_short[-1]
        print('Get the name of a twitter-user: ', name_short)
        last_parse = int(time.time())
        caunt_total = [name_short, club_names, last_parse]
        cur.execute('INSERT INTO Total_Table VALUES(?, ?, ?)', caunt_total)
        con.commit()
        print('Record in table Total_Table about time parsing. User: ', name_short)
        print('Check for positive and negative words of the user: ', name_short)
        brain_bot(name_short, club_names, count_twitts)
p = Path(__file__).parents[0]
chdir(p)
cur.close()
con.close()
print('Finished work and disconnected from the database: ', db_name)
