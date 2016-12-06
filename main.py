from flask import Flask, render_template, abort, request
import sys
from twython import Twython
from dictionary import Dictionary

APP_KEY = '<INSERT APP_KEY>'
APP_SECRET = '<INSERT APP SECRET>'

twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()

twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

app = Flask(__name__)

class SentimentScore:
    def __init__(self, positive_tweets, negative_tweets, neutral_tweets):

        self.positive_tweets = positive_tweets
        self.negative_tweets = negative_tweets
        self.neutral_tweets = neutral_tweets

        self.neg = len(negative_tweets)
        self.pos = len(positive_tweets)
        self.neut = len(neutral_tweets)




dictionaryN = Dictionary('negative-words.txt')

dictionaryP = Dictionary('positive-words.txt')

def sentiment(tweet):

    negative_score = 0
    positive_score = 0

    tweet_words = tweet.split()

    for word in tweet_words:
        negative_score += dictionaryN.check(word)

    for word in tweet_words:
        positive_score += dictionaryP.check(word)

    if negative_score > positive_score:
        return 'negative'
    elif negative_score == positive_score:
        return 'neutral'
    else:
        return 'positive'

    # use dictionary to count negative frequent

def sentiment_analysis(tweets):

    negative_tweets = []
    positive_tweets = []
    neutral_tweets = []

    for tweet in tweets:

        res = sentiment(tweet['text'])

        if res == 'negative':
            negative_tweets.append(tweet['text'])
        elif res == 'positive':
            positive_tweets.append(tweet['text'])
        else:
            neutral_tweets.append(tweet['text'])

    return SentimentScore(positive_tweets, negative_tweets, neutral_tweets)


@app.route("/", methods=["POST","GET"])
def root():

    if request.method == "POST":

        user_timeline = twitter.get_user_timeline(screen_name=request.form['twitter_username'], count = 100)

        return render_template("result.html", result=sentiment_analysis(user_timeline), username=request.form['twitter_username'])
    else:
        return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


app.run(debug=True)
