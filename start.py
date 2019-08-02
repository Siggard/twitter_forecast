import tweepy
import os
import glob

consumer_key = 'gijaNPO1RVGy2lKkCUxUw'
consumer_secret = 'gWCy6OIpHYGhSMrj0D5pjOmnJQP55M7BF0X35T6XMQ'
access_token = '363931816-LGB5m13W9oxdj8ktG3eBw1box4W0YBLqI4FP8PkL'
access_token_secret = 'zgBBsmYczXncka89ONP7LfyeZbdl7cYeE4cRGEh5TeA'
path_to_dir = 'clubs'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
#in 'count_twitts' until you manually set the number of tweets
def twitts_user(user_name, count_twitts = 3):
   api = tweepy.API(auth)
   user = api.get_user(user_name)
   screen_name_user = user.screen_name
   twitter_user_id = user.id 
   public_tweets = api.user_timeline(user_name, count = count_twitts)
   for tweet in public_tweets:
      print(tweet.text)

#specify the directory and search for text files
os.chdir(path_to_dir) 
for file in glob.glob("*.txt"):
    #read lines in file
    #print("\nFile: " + file + "\n")
    file_open = open(file)
    for line in file_open:
        #print('String: ' + line)
        #trim the link
        name_long = list(line)				
        for i in range(0,20):
            del name_long[0]			
        name_short = '' . join(name_long)
        print("\n" + name_short + " =====>>> ")
        twitts_user(name_short)