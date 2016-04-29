import os
import sys
import logging
import json
import pymongo
from flask import Flask, Response, render_template, request, redirect, url_for, send_from_directory, g, session
from bokeh.resources import INLINE
from test import test
from classify import *
from sampleCollection import *
from bokehGraph import plot
from speechRecognition import speak

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
inpTweets = csv.reader(open('data/training_dataset.csv', 'rt'), delimiter=',', quotechar='|')
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
    return render_template('home.html')

@webapp.route("/dashboard", methods=['GET','POST'])
def dashboard():
    
    # Test the classifier
    if request.method == 'POST':
        testTweet = request.form["tweet"]
    else:
        testTweet = ""
    if(testTweet):
        processedTestTweet = processTweet(testTweet)
        sentiment = NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet, stopWords)))
        print ("testTweet = %s, sentiment = %s\n"% (testTweet, sentiment))
    else:
        sentiment = ""

    
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

    data = []
    bar = []

    upload(keyWord,numTweets)
    data = count_sent(NBClassifier)
    bar = plot(data)

    print ("keyword = %s, number of tweets = %s\n"% (keyWord, numTweets))
    print("sentiment: pos = %s neut = %s neg = %s\n"% (data[0].pos, data[0].neut, data[0].neg))
    print("tweets: \n")
    for n in range(int(numTweets) - 1):
        print("%s\n"% data[1][n].text)
    results = [keyWord, numTweets]
    return render_template('index.html', 
        key_results=results,
        twit_data = data,
        plot_script=bar[0],
        plot_div=bar[1],
        js_resources=bar[2],
        css_resources=bar[3])

@webapp.route("/speech", methods=['GET','POST'])
def speech_recogn():

    speechToText = ""
    sentiment = ""

    if request.method == 'POST':
        speechToText = speak()
    if(speechToText):
        processedText = processTweet(speechToText)
        sentiment = NBClassifier.classify(extract_features(getFeatureVector(processedText, stopWords)))    

    textObj = [speechToText, sentiment]

    return render_template('index.html',speech_results = textObj)

#server initializiation
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 33507))
    webapp.run(host='0.0.0.0', port=port, debug=True)
