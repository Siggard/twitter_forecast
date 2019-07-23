str = "test"
print("Hello %s" % str)

import tweepy


consumer_key = 'gijaNPO1RVGy2lKkCUxUw';
consumer_secret = 'gWCy6OIpHYGhSMrj0D5pjOmnJQP55M7BF0X35T6XMQ';
access_token = '363931816-LGB5m13W9oxdj8ktG3eBw1box4W0YBLqI4FP8PkL';
access_token_secret = 'zgBBsmYczXncka89ONP7LfyeZbdl7cYeE4cRGEh5TeA';


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)