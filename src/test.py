#tests the output from the database

import json
import pymongo


#sample databse, can only store 500MB
MONGO_DB_URI = "mongodb://test_user:1234@ds053300.mlab.com:53300/emotwit2016"
client = pymongo.MongoClient(MONGO_DB_URI)
db = client.emotwit2016

tw = open("twitter_data.txt","r+")

def test():
    tweets_iterator = db.twitter_collection.find()
    twit_data = {}
    i = 0
    for tweet in tweets_iterator:
        if 'text' in tweet:
            #tw.write(tweet['text']+ "\n")
            twit_data[i] = tweet['text']
            ++i
        else:
            print ('This does not have a text entry')
    return twit_data
