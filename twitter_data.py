import tweepy as tw
import json
from dotenv import load_dotenv
import os
from datetime import datetime as dt
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from cleantext import clean

from elasticsearch import Elasticsearch


def sieve(word_list):
    # remove stopwords
    stop_words = set(stopwords.words('english'))
    new_list = [word for word in word_list if word not in stop_words]
    new_list = [word for word in new_list if not word.startswith('http')]
    new_list = [word for word in new_list if not word.startswith('RT')]
    new_list = [word for word in new_list if not word.startswith('@')]
    new_list = [clean(word, no_emoji=True, no_punct=True, replace_with_punct=" ") for word in new_list]
    new_list = [word for word in new_list if not word.isdigit()]
    new_list = [word for word in new_list if len(word) > 2]
    new_list = [i for i in new_list if i]
    print(new_list)
    return new_list


load_dotenv()

twitter_cred = dict()
twitter_cred["CONSUMER_KEY"] = os.getenv('consumer_key')
twitter_cred["CONSUMER_SECRET"] = os.getenv('consumer_secret')
twitter_cred["ACCESS_KEY"] = os.getenv('access_token')
twitter_cred["ACCESS_SECRET"] = os.getenv('access_token_secret')

auth = tw.OAuthHandler(
    twitter_cred["CONSUMER_KEY"], twitter_cred["CONSUMER_SECRET"])
auth.set_access_token(
    twitter_cred["ACCESS_KEY"], twitter_cred["ACCESS_SECRET"])
api = tw.API(auth, wait_on_rate_limit=True)


es = Elasticsearch("http://localhost:9200")


class StreamAPI(tw.StreamingClient):
    def on_data(self, raw_data):
        json_data = json.loads(raw_data)
        print(json_data['data']['text'])
        doc = {
            '@timestamp': dt.now(),
            'text': json_data['data']['text'],
            'word_list': sieve(json_data['data']['text'].split(' '))
        }
        print()
        es.index(index="betaa", document=doc)

def live_fetch():
    streamer = StreamAPI(os.getenv('bearer_token'))
    for rule in streamer.get_rules().data:
        streamer.delete_rules(rule.id)
    print(streamer.get_rules())
    rules = []
    rules.append("#shop OR #shopping OR #sale OR #sale OR #flipkart OR #fashion")
    # rules.append("from:godofgeeks_")
    for rule in rules:
        streamer.add_rules(tw.StreamRule(rule))
    streamer.filter()


def static_search():
    client = tw.Client(os.getenv('bearer_token'))
    query = '#shop OR #shopping OR #sale OR #sale OR #flipkart OR #fashion lang:en'
    tweets = tw.Paginator(client.search_recent_tweets, query=query,
                            tweet_fields=['context_annotations', 'created_at'], max_results=100).flatten(limit=100)
    for tweet in tweets:
        # print(tweet.text)
        doc = {
            '@timestamp': dt.now(),
            'created_at': tweet.created_at,
            'text': tweet.text,
            'word_list': sieve(tweet.text.split(' '))
        }
        print()
        es.index(index="sampleindex", document=doc)


static_search()