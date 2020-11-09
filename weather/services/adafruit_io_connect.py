from Adafruit_IO import Client, Feed, RequestError
from datetime import datetime
import logging


def create_feed_connection(aio: Client, feed_name: str):
    try:
        return aio.feeds(feed_name)
        logging.info("[{0}] Connected to {1} feed".format(datetime.now(), feed_name))
    except RequestError: # Doesn't exist, create a new feed
        feed = Feed(name=feed_name)
        logging.info("[{0}] Created {1} feed".format(datetime.now(), feed_name))
        return aio.create_feed(feed)

