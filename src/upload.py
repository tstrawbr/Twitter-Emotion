
#Only run this script in order store additional tweets in the database
#fyi our databse is a free MongoLab instance with only 500MB


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pymongo
import tweepy


consumer_token = "BeqEzsvFjeJzTC9LeSTOtHGoO"
consumer_secret = "sejQngohmybkGexNI69qNeJfRA513wK8MA5Otmdm8CBEk5K5Ha"
key = 	"412672432-LqNFAoCjARGX5Wg2qX2RvWQT6x2cKpDH5RXHSF5K"
secret =  "ovFhfeqgKb37neFRHxCXAcZUAnffqiry9wlZfzKnsQui0"


MONGO_DB_URI = "mongodb://test_user:1234@ds053300.mlab.com:53300/emotwit2016"
client = pymongo.MongoClient(MONGO_DB_URI)
db = client.emotwit2016

class StdOutListener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data)
        collection = db['twitter_collection']
        collection.insert(tweet)
        #print(tweet)
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(key, secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords:
    stream.filter(track=['angry', 'sad', 'happy'])
