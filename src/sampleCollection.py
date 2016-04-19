from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy

# Consumer keys and access tokens, used for OAuth
consumer_key = '*'
consumer_secret = 'x'
access_token = 'x'
access_token_secret = 'x'
 
# OAuth process, using the keys and tokens
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


#get limit and subject from HTTP source
#do with get instead of input
    
userTrack = input('Enter tweet subject')
userLimit = input('Enter number of tweets')

def __init__(self, api=tweepy.API([auth], # support for multiple authentication handlers    
                 retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]),  
                  monitor_rate_limit=True, wait_on_rate_limit=True)):
    super(StdOutListener, self).__init__()
    self.num_tweets = 0

class StdOutListener(StreamListener):

    def on_data(self, data):
        self.num_tweets += 1
        if self.num_tweets < userLimit:
            with open('tweets.txt','a') as tf:
                tf.write(data)
            return True

    def on_error(self, status):
        print (status)
        
        
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterStream = Stream(auth, StdOutListener())
twitterStream.filter(track=[userTrack])