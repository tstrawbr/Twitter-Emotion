from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

# Consumer keys and access tokens, used for OAuth
consumer_key = 'C9QOyOB0G6IOU6UvtRafXE9xt'
consumer_secret = 'm6eEobiGEEHXhJjocnjKu3Oc6j78eJAYNis83Q1BYUXAKWO7pe'
access_token = '865504190-sNubkyEN9lLltdSwOKlso4gBiBrwjr8K0zkXf7cI'
access_token_secret = 'ywFM2osQLdQtXWFkBDkICvskCCYuGpW89ReOJgiWpmJ4P'
 
# OAuth process, using the keys and tokens
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


#get limit and subject from HTTP source
#do with get instead of input
    
userTrack = input('Enter tweet subject')
userLimit = input('Enter number of tweets')

#tweepy.API([auth], # support for multiple authentication handlers    
                 #retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]), wait_on_rate_limit=True


class StdOutListener(StreamListener): 
    
    
    def __init__(self, api=None):
        super(StdOutListener, self).__init__()
        self.num_tweets=0
    
    def on_status(self, status):
        self.num_tweets += 1        
        if self.num_tweets < int(userLimit):
            with open('tweets.txt','a') as tf:
                line = (status.text).encode('utf-8')
                tf.write(str(line))
                tf.write(' || ')
            return True
        else:
            return False

    def on_error(self, data):
        print (data)
        
        
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterStream = Stream(auth, StdOutListener())
twitterStream.filter(track=[userTrack])