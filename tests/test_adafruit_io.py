from Adafruit_IO import Client, Feed, RequestError
from dotenv import load_dotenv
import unittest
import os
from random import randint

class Test_TestAdafruitIO(unittest.TestCase):
    def test_adafruit_io_feed(self):
        load_dotenv(verbose=True)

        KEY = os.getenv("ADAFRUIT_IO_KEY")
        USERNAME = os.getenv("ADAFRUIT_IO_USERNAME")
        aio = Client(USERNAME, KEY)

        try:
            test = aio.feeds("test")
        except RequestError: # Doesn't exist, create a new feed
            feed = Feed(name="test")
            test = aio.create_feed(feed)

        for i in range(5):
            value = randint(0, 50)
            aio.send_data(test.key, value)

        data = aio.receive(test.key)
        self.assertIsNotNone(data.value)

        