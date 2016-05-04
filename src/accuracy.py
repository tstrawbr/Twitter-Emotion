from classify import *
#from test import test
import itertools
from nltk.tokenize import word_tokenize


#start extract_features
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureListTrain:
        features['contains(%s)' % word] = (word in tweet_words)
    return features
#end
#start extract_features
def extract_features2(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featTest:
        features['contains(%s)' % word] = (word in tweet_words)
    return features
#end

#Read the tweets one by one and process it
inpTweets = csv.reader(open('data/training_dataset.csv', 'rt', encoding = "utf-8"), delimiter=',', quotechar='|')
inpTweetsTest = csv.reader(open('data/training_dataset.csv', 'rt', encoding = "utf-8"), delimiter=',', quotechar='|')
stopWords = getStopWordList('data/stopwords.txt')
count = 0;
featureListTrain = []
featTest = []
tweetsTrain = []
tweetsTest = []
for row in inpTweets:
    sentiment = row[0]
    tweet = row[1]
    processedTweet = processTweet(tweet)
    featureVector = getFeatureVector(processedTweet, stopWords)
    featureListTrain.extend(featureVector)
    tweetsTrain.append((featureVector, sentiment));
#end loop
    
for row in inpTweetsTest:
    sentiment = row[0]
    tweet = row[1]
    processedTweet = processTweet(tweet)
    featureVector = getFeatureVector(processedTweet, stopWords)
    featTest.extend(featureVector)
    tweetsTest.append((featureVector, sentiment));
#end loop

# Remove featureList duplicates
featureListTrain = list(set(featureListTrain))
featTest = list(set(featTest))

# Generate the training set
training_set = nltk.classify.util.apply_features(extract_features, tweetsTrain)
testing_set = nltk.classify.util.apply_features(extract_features2, tweetsTest)

# Train the Naive Bayes classifier
NBClassifier = nltk.NaiveBayesClassifier.train(training_set)

print("Classifier accuracy percent:",(nltk.classify.accuracy(NBClassifier, testing_set))*100)

