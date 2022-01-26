#coding: utf-8

import random
import time
from urllib.parse import urljoin
import logging

import requests

REDDIT = "https://www.reddit.com"
DEFAULTDOG = "https://i.redd.it/bqkh6gdv5so01.jpg"
logger = logging.getLogger(__name__)

dogreddits = [
    "PuppySmiles",
    "dogpictures"
]

def urls(result):
    return [a['data']['url'] for a in result['data']['children']]

def get_dogpics():
    session = requests.Session()
    session.headers.update({'User-Agent': 'This is /u/benediktkr fetching two dog pictures'})

    dogs = []
    for subreddit in dogreddits:
        d = session.get(urljoin(REDDIT, "/r/{}/.json".format(subreddit)))
        if d.status_code == 200:
            dogs.extend(urls(d.json()))

        logger.debug("Sleeping for 3 seconds between hitting reddit")
        time.sleep(3.0)

    logging.info("Found {} dogs".format(len(dogs)))
    return dogs

def get_random_dogpic():
    try:
        dogs = get_dogpics()
        rnddog = random.choice(dogs)
        logging.info("Picked {}".format(rnddog))
        return rnddog
    except IndexError as e:
        # get_dogpics() returned an empty list
        logging.error(e)
        logging.info("Picking default dog")
        return DEFAULTDOG
    except requests.exceptions.RequestException as e:
        logging.error(e)
        logging.info("Picking default dog")
        return DEFAULTDOG

if __name__ == "__main__":
    print("Default:", DEFAULTDOG)
    print(get_random_dogpic())
