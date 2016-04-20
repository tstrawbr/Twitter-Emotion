import os
import sys
import logging
import json
import pymongo
from flask import Flask, Response, render_template, request, redirect, url_for, send_from_directory, g, session
from test import test
from classify import *
MONGO_DB_URI = "mongodb://test_user:1234@ds053300.mlab.com:53300/emotwit2016"
client = pymongo.MongoClient(MONGO_DB_URI)
db = client.emotwit2016

#start extract_features
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features
#end

#Read the tweets one by one and process it
inpTweets = csv.reader(open('data/sampleTweets.csv', 'rt'), delimiter=',', quotechar='|')
stopWords = getStopWordList('data/stopwords.txt')
count = 0;
featureList = []
tweets = []
for row in inpTweets:
    sentiment = row[0]
    tweet = row[1]
    processedTweet = processTweet(tweet)
    featureVector = getFeatureVector(processedTweet, stopWords)
    featureList.extend(featureVector)
    tweets.append((featureVector, sentiment));
#end loop

# Remove featureList duplicates
featureList = list(set(featureList))

# Generate the training set
training_set = nltk.classify.util.apply_features(extract_features, tweets)

# Train the Naive Bayes classifier
NBClassifier = nltk.NaiveBayesClassifier.train(training_set)


webapp = Flask(__name__)
@webapp.route("/", methods=['GET','POST'])
def root():
    
    # Test the classifier
    if request.method == 'POST':
        testTweet = request.form["tweet"]
    else:
        testTweet = 'Congrats bobbie!'

    processedTestTweet = processTweet(testTweet)
    sentiment = NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet, stopWords)))
    print ("testTweet = %s, sentiment = %s\n"% (testTweet, sentiment))

    results = [testTweet, sentiment]
    return render_template('index.html', results=results)



#API Routes
#General format is "/api/<endpoint here>"


@webapp.route("/keyword", methods=['GET','POST'])
def api_test():

    # Test the classifier
    if request.method == 'POST':
        keyWord = request.form["keyword"]
        numTweets = request.form["options"]
    else:
        keyWord = 'dog'
        numTweets = 15

    processedTestTweet = processTweet(keyWord)
    sentiment = NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet, stopWords)))
    print ("keyword = %s, number of tweets = %s\n"% (keyWord, numTweets))

    results = [keyWord, numTweets]
    return render_template('index.html', key_results=results)

#server initializiation
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 33507))
    webapp.run(host='0.0.0.0', port=port, debug=True)
