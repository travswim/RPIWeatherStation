# Dependencies
from time import sleep
import os
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from logging.handlers import RotatingFileHandler
import threading
from datetime import datetime
from Adafruit_IO import Client, Feed, RequestError


# Sensor connections
from weather.sensors.RG11 import RG11, is_any_thread_alive, get_RG11, reset_RG11
from weather.sensors.i2c_devices import BME280, PM25
from weather.sensors.wind_speed import anemometer, get_wind_speed, reset_wind_speed
from weather.sensors.wind_direction import voltage, voltage_to_degrees, voltage_to_direction

# Settings
from weather.settings import get_env, internet


# Global Variables
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

# [x] TODO: Python app file/folder structure
# [ ] TODO: Integrate PM2.5 Sensor readings
# [ ] TODO: Logging - python
# [ ] TODO: Logging - GCP
# [x] TODO: Collect weather data
# [ ] TODO: Schedule every 15min
# [ ] TODO: Reset Rainfall counter
# [ ] TODO: Reset windspeed
# [ ] TODO: Fix fritzing diagrams for perf board

def reset_logs():
    fname = 'weather.log'
    with open(fname) as f:
        for i, _ in enumerate(f):
            pass
    del_lines = i+1
    a_file = open(fname, "r")
    lines = a_file.readlines()
    a_file.close()

    del lines[:del_lines]

    new_file = open(fname, "w+")

    for line in lines:

        new_file.write(line)

    new_file.close()


def get_weather():
    # Get temperature, humidity, pressureasd
    temperature, humidity, pressure = BME280()
    print("\nTemperature: %0.1f C" % temperature)
    print("Humidity: %0.1f %%" % humidity)
    print("Pressure: %0.1f hPa" % pressure)

    # Particle Air Quality
    pm10, pm25, pm100 = PM25()
    print("Concentration Units (standard)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (pm10, pm25, pm100)
    )

    # Wind Direction
    chan = voltage()
    degree_sign= u'\N{DEGREE SIGN}'
    print('Direction: ' + voltage_to_direction(chan.voltage))
    print('Direction: ' + str(voltage_to_degrees(chan.voltage)) + degree_sign)
    
    # Rainfall
    print("Rainfall: " + str(get_RG11()) + "mm")

    # Wind Speed
    wind_speed, max_wind_speed, min_wind_speed = get_wind_speed()
    print("Wind Speed: " + str(wind_speed) + "KPH\n" + "Max Wind Speed: " + str(max_wind_speed) + "KPH\n" + "Min Wind Speed: " + str(min_wind_speed) + "KPH")

def run():
    """
    Driver function
    """
    # Start logging
    logging.basicConfig(filename='weather.log', level=logging.INFO)
    
    # Check internet connection
    while not internet():
        logging.error("[{}] No internet connection".format(datetime.now()))
        sleep(10)
    logging.info("[{}] Connected to internet".format(datetime.now()))
    # Start monitoring rainfall from the RG11
    run_RG11 = threading.Thread(target=RG11, name="RG11", daemon=True)
    run_RG11.start()
    logging.info("[{}] Started RG11".format(datetime.now()))

    # Start monitoring the wind speed from the anemometer
    run_anemometer = threading.Thread(target=anemometer, name="Anemometer", daemon=True)
    run_anemometer.start()
    logging.info("[{}] Started anemometer wind speed".format(datetime.now()))


    scheduler = BackgroundScheduler()
    
    # Testing
    # scheduler.add_job(get_weather, 'cron', second=0)
    # scheduler.add_job(get_weather, 'cron', second=10)
    # scheduler.add_job(get_weather, 'cron', second=20)
    # scheduler.add_job(get_weather, 'cron', second=30)
    # scheduler.add_job(get_weather, 'cron', second=40)
    # scheduler.add_job(get_weather, 'cron', second=50)

    # Reset
    scheduler.add_job(reset_RG11, 'cron', hour=0)
    scheduler.add_job(reset_wind_speed, 'cron', hour=0)
    scheduler.add_job(reset_logs, 'cron', hour=0)
    
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    
    


    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        ADAFRUIT_IO_KEY, ADAFRUIT_IO_USERNAME, LOCATION_LATITUDE, LOCATION_LONGITUDE, LOCATION_ELEVATION = get_env()
        # Create an instance of the REST client.
        aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
        # location/elevation
        metadata = {'lat': LOCATION_LATITUDE,
                'lon': LOCATION_LONGITUDE,
                'ele': LOCATION_ELEVATION,
                'created_at': None}

        # STARTUP CONNECTION TO ADAFRUIT IO

        # temperature
        try:
            temperature = aio.feeds(TEMERATURE_FEED)
        except RequestError: # Doesn't exist, create a new feed
            feed = Feed(name=TEMERATURE_FEED)
            temperature = aio.create_feed(feed)
        
        # humidity
        try:
            humidity = aio.feeds(HUMIDITY_FEED)
        except RequestError: # Doesn't exist, create a new feed
            feed = Feed(name=HUMIDITY_FEED)
            humidity = aio.create_feed(feed)

        # pressure
        try:
            pressure = aio.feeds(PRESSURE_FEED)
        except RequestError: # Doesn't exist, create a new feed
            feed = Feed(name=PRESSURE_FEED)
            pressure = aio.create_feed(feed)

        # rainfall
        try:
            rainfall = aio.feeds(RAINFALL_FEED)
        except RequestError: # Doesn't exist, create a new feed
            feed = Feed(name=RAINFALL_FEED)
            rainfall = aio.create_feed(feed)

        # windspeed
        try:
            wind_speed = aio.feeds(WINDSPEED_FEED)
        except RequestError: # Doesn't exist, create a new feed
            feed = Feed(name=WINDSPEED_FEED)
            wind_speed = aio.create_feed(feed)

        # winddirection
        try:
            winddirection = aio.feeds(WINDDIRECTION_FEED)
        except RequestError: # Doesn't exist, create a new feed
            feed = Feed(name=WINDDIRECTION_FEED)
            winddirection = aio.create_feed(feed)

        # Air quality pm1.0
        try:
            aq_pm10 = aio.feeds(AIR_QUALITY_PM10)
        except RequestError: # Doesn't exist, create a new feed
            feed = Feed(name=AIR_QUALITY_PM10)
            aq_pm10 = aio.create_feed(feed)
        
        # Air quality pm2.5
        try:
            aq_pm25 = aio.feeds(AIR_QUALITY_PM25)
        except RequestError: # Doesn't exist, create a new feed
            feed = Feed(name=AIR_QUALITY_PM25)
            aq_pm25 = aio.create_feed(feed)

        # Air quality pm10.0
        try:
            aq_pm100 = aio.feeds(AIR_QUALITY_PM100)
        except RequestError: # Doesn't exist, create a new feed
            feed = Feed(name=AIR_QUALITY_PM100)
            aq_pm100 = aio.create_feed(feed)

        while True:
            
            print("Sent Data: 9 data points")
            # SENSOR READINGS
            try:
                # Temperature, humidity, pressure
                temp, hum, press = BME280()
                
                aio.send_data(temperature.key, temp, metadata)
                aio.send_data(humidity.key, hum, metadata)
                aio.send_data(pressure.key, press, metadata)

                # Air quality
                pm10, pm25, pm100 = PM25()
                aio.send_data(aq_pm10.key, pm10, metadata)
                aio.send_data(aq_pm25.key, pm25, metadata)
                aio.send_data(aq_pm100.key, pm100, metadata)

                # Wind direction
                chan = voltage()
                aio.send_data(winddirection.key, voltage_to_direction(chan.voltage), metadata)

                # Wind speed
                ws, _, _ = get_wind_speed()
                aio.send_data(wind_speed.key, ws, metadata)

                # Rainfall
                get_RG11()
                aio.send_data(rainfall.key, get_RG11(), metadata)
            except:
                logging.warning("Reached data limit. Wating for 1min")
                sleep(60)

            sleep(20)


               
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown() 

    

    

# if __name__ == '__main__':
#     reset_logs()