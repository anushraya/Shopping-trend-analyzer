from pprint import pp
from dotenv import load_dotenv
import os
from instagrapi import Client
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from cleantext import clean
from elasticsearch import Elasticsearch
from datetime import datetime as dt
import json

def sieve(word_list):
    stop_words = set(stopwords.words('english'))
    new_list = [word for word in word_list if word not in stop_words]
    new_list = [word for word in new_list if not word.startswith('http')]
    new_list = [word for word in new_list if not word.startswith('@')]
    new_list = [clean(word, no_emoji=True, no_punct=True, replace_with_punct=" ") for word in new_list]
    new_list = [word for word in new_list if not word.isdigit()]
    new_list = [word for word in new_list if len(word) > 2]
    new_list = [i for i in new_list if i]
    # print(new_list)
    return new_list


load_dotenv()

cl = Client()
cl.login(os.getenv('username'), os.getenv('password'))

es = Elasticsearch("http://localhost:9200")

# hashtag = cl.hashtag_info('fashion')
# print(hashtag.dict())

medias = cl.hashtag_medias_top('fashion', amount=200)
# medias = cl.hashtag_medias_recent('fashion', amount=2)
for media in medias:
    # pp(media.dict())
    print(sieve(media.dict()['caption_text'].split(' ')))
    doc = {
            '@timestamp': dt.now(),
            'text': media.dict()['caption_text'],
            'word_list': sieve(media.dict()['caption_text'].split(' '))
        }
    es.index(index="sampleindex", document=doc)
    print()
