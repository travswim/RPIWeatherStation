from Adafruit_IO import Client, Feed, RequestError


global TEMERATURE_FEED
global HUMIDITY_FEED
global PRESSURE_FEED
global RAINFALL_FEED
global WINDSPEED_FEED 
global WINDDIRECTION_FEED
global AIR_QUALITY_PM10
global AIR_QUALITY_PM25
global AIR_QUALITY_PM100 


TEMERATURE_FEED = "temperature"
HUMIDITY_FEED = "humidity"
PRESSURE_FEED = "pressure"
RAINFALL_FEED = "rainfall"
WINDSPEED_FEED = "windspeed"
WINDDIRECTION_FEED = "winddirection"
AIR_QUALITY_PM10 = "pm10"
AIR_QUALITY_PM25 = "pm25"
AIR_QUALITY_PM100 = "pm100"
# [x] TODO: Check if feeds created, if not create feeds
# [ ] TODO: Upload data to feeds


def adafruit_io_startup(username: str, key: str, feed_type) -> Client:    

    aio = Client(username, key)
    try:
        weather_feed = aio.feeds(feed_type)
    except RequestError: # Doesn't exist, create a new feed
        feed = Feed(name=TEMERATURE_FEED)
        weather_feed = aio.create_feed(feed)
    
    return aio

    
    
    while True:
        value = randint(0, 50)
        # Set metadata associated with value
        metadata = {'lat': 40.726190,
                'lon': -74.005334,
                'ele': -6,
                'created_at': None}
        aio.send_data(temperature.key, value, metadata)
        sleep(2)
    


def adafruit_io_update_feed(feed: Client, data_val, metadata) -> None:
    

if __name__ == "__main__":
    ADAFRUIT_IO_KEY = "travswim"
    ADAFRUIT_IO_USERNAME = "aio_xYFp68kz9mO8LiXNM1aIm0LqObel"
    adafruit_io_startup(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)