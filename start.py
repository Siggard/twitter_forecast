import tweepy
import os
import glob


consumer_key = 'gijaNPO1RVGy2lKkCUxUw';
consumer_secret = 'gWCy6OIpHYGhSMrj0D5pjOmnJQP55M7BF0X35T6XMQ';
access_token = '363931816-LGB5m13W9oxdj8ktG3eBw1box4W0YBLqI4FP8PkL';
access_token_secret = 'zgBBsmYczXncka89ONP7LfyeZbdl7cYeE4cRGEh5TeA';
path_to_dir = 'clubs';

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#specify the directory and search for text files
os.chdir(path_to_dir) 
for file in glob.glob("*.txt"):
	#read lines in file
	print("\nFile: " + file + "\n")
	file_open = open(file)
	for line in file_open:
		#tweepy API work, connect to account and take feed
		print("String: " + line)

#api = tweepy.API(auth)
#public_tweets = api.home_timeline()
#for tweet in public_tweets:
   #print(tweet.text)
