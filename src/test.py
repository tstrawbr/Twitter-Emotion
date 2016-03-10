#tests the output from the database

import json
import pymongo


#sample databse, can only store 500MB
MONGO_DB_URI = "mongodb://test_user:1234@ds053300.mlab.com:53300/emotwit2016"
client = pymongo.MongoClient(MONGO_DB_URI)
db = client.emotwit2016

tw = open("twitter_data.txt","r+")

tweets_iterator = db.twitter_collection.find()
for tweet in tweets_iterator:
    if 'text' in tweet:
        tw.write(tweet['text']+ "\n")
    else:
        print ('This does not have a text entry')
