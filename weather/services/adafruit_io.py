from Adafruit_IO import Client, Feed
import json



# [ ] TODO: Check if feeds created, if not create feeds
# [ ] TODO: Upload data to feeds


def adafruit_io_startup(key: str, username: str) -> None:
    aio = Client(username, key)
    feeds = aio.feeds()
    groups = aio.groups()
    # print(json.dumps(feeds[0], indent=4))
    print(feeds[0])
    print(groups)
    


# def adafruit_io_update_feed(feed: str) -> None:


if __name__ == "__main__":
    ADAFRUIT_IO_KEY = "travswim"
    ADAFRUIT_IO_USERNAME = "aio_kCMI35aAHW0TwxWkLaR6tu9bDB4N"
    adafruit_io_startup(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)