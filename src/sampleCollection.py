from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from classify import *
from main import extract_features

class tweet(object):
    text = ""
    sentiment = ""
class sentSum(object):
    pos = 0
    neg = 0
    neut = 0

def upload(userTrack,userLimit):
    # Consumer keys and access tokens, used for OAuth
    consumer_key = 'BeqEzsvFjeJzTC9LeSTOtHGoO'
    consumer_secret = 'sejQngohmybkGexNI69qNeJfRA513wK8MA5Otmdm8CBEk5K5Ha'
    access_token = '412672432-LqNFAoCjARGX5Wg2qX2RvWQT6x2cKpDH5RXHSF5K'
    access_token_secret = 'ovFhfeqgKb37neFRHxCXAcZUAnffqiry9wlZfzKnsQui0'
     
    # OAuth process, using the keys and tokens
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)


    #get limit and subject from HTTP source
    #do with get instead of input
        
    #userTrack = input('Enter tweet subject')
    #userLimit = input('Enter number of tweets')

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
                    tf.write(' | ')
                    tf.write(str(line))
                    tf.write('|\n')
                return True
            else:
                return False

        def on_error(self, data):
            print (data)
            
            
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    twitterStream = Stream(auth, StdOutListener())
    twitterStream.filter(track=[userTrack])

def count_sent(NBClassifier):
    stopWords = getStopWordList('data/stopwords.txt')
    inpTweets = csv.reader(open('tweets.txt', 'rt'), quotechar='|')
    twitArray = []
    twitSum = sentSum()
    for row in inpTweets:
        processedTestTweet = processTweet(row[0])
        sentiment = NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet, stopWords)))
        if sentiment =='positive':
            twitSum.pos += 1
        elif sentiment =='negative':
            twitSum.neg += 1
        elif sentiment =='neutral':
            twitSum.neut += 1
        tweetObj = tweet()
        tweetObj.text = row[0]
        tweetObj.sentiment = sentiment
        twitArray.append(tweetObj)

    #returns sum of sentiments and the actual tweets
    result = [twitSum,twitArray]
    open('tweets.txt', 'w').close()
    return result

        
