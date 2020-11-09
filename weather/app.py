# Dependencies
from time import sleep
import os
import sys
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
from weather.services.adafruit_io_connect import create_feed_connection

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
REFRESH_RATE = 30

# [x] TODO: Python app file/folder structure
# [x] TODO: Integrate PM2.5 Sensor readings
# [ ] TODO: Logging - python
# [ ] TODO: Error handling
# [x] TODO: Collect weather data
# [x] TODO: Schedule every 20s
# [x] TODO: Reset Rainfall counter
# [x] TODO: Reset windspeed
# [ ] TODO: Fix fritzing diagrams for perf board

def reset_logs() -> None:
    """
    Deletest 1/2 the log data to ensure that the file does not get too large

    Arguments: None

    Returns: None
    """
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

def send_feed_data(aio: Client, metadata: dict, temperature: Feed, humidity: Feed, pressure: Feed, rainfall: Feed, wind_speed: Feed, wind_direction: Feed, aq_pm10: Feed, aq_pm25: Feed, aq_pm100: Feed) -> None:
    """
    Sends collected sensor data to their respective Adafruit IO feeds

    Arguments:
        - aio: The Adafruit IO client connection
        - metadata: The location metadata to be sent with each data point
        - temperature: the temperature feed
        - humidity: the humidity feed
        - pressure: the pressure feed
        - rainfall: the rainfall feed
        - wind_speed: the wind_speed feed
        - wind_direction: the wind_direction feed
        - aq_pm10: the air quality 1.0um index feed
        - aq_pm25: the air quality 2.5um index feed
        - aq_pm100: the air quality 10.0um index feed

    Returns: None
      
    """

    # SENSOR READINGS: Send data to feeds
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
        aio.send_data(wind_direction.key, voltage_to_direction(chan.voltage), metadata)

        # Wind speed
        ws, _, _ = get_wind_speed()
        aio.send_data(wind_speed.key, ws, metadata)

        # Rainfall
        get_RG11()
        aio.send_data(rainfall.key, get_RG11(), metadata)
        logging.info("[{}] Sensor data sent to feeds".format(datetime.now()))
    except:
        logging.error("Could not send data to Adafruit IO. Exiting System")
        sys.exit(1)


def print_weather() -> None:
    """
    Helper printer function that helps with debugging

    Arguments: None

    Returns: None
    """
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

def run() -> None:
    """
    Driver function. Main function that logs weather data
    """
    # Start logging
    logging.basicConfig(filename='weather.log', level=logging.INFO)
    
    # Check internet connection
    while not internet():
        logging.error("[{}] No internet connection".format(datetime.now()))
        sleep(60)
    logging.info("[{}] Connected to internet".format(datetime.now()))

    # Start monitoring rainfall from the RG11
    try:
        run_RG11 = threading.Thread(target=RG11, name="RG11", daemon=True)
        run_RG11.start()
        logging.info("[{}] Started RG11".format(datetime.now()))
    except:
        logging.error("Could not start RG11")
        sys.exit(1)

    # Start monitoring the wind speed from the anemometer
    try:
        run_anemometer = threading.Thread(target=anemometer, name="Anemometer", args=[30], daemon=True)
        run_anemometer.start()
        logging.info("[{}] Started anemometer wind speed".format(datetime.now()))
    except:
        logging.error("Could not start anemometer wind speed")
        sys.exit(1)


    
    
    # Get environment parameters
    ADAFRUIT_IO_KEY, ADAFRUIT_IO_USERNAME, LOCATION_LATITUDE, LOCATION_LONGITUDE, LOCATION_ELEVATION = get_env()
    
    # Create an instance of the REST client.
    try:
        aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
        logging.info("[{}] Connection to Adafruit IO established".format(datetime.now()))

    except:
        # Failing gracefully
        logging.info("[{}] Failed to connect to Adafruit IO".format(datetime.now()))
        sys.exit(1)

    # location/elevation
    metadata = {'lat': LOCATION_LATITUDE,
            'lon': LOCATION_LONGITUDE,
            'ele': LOCATION_ELEVATION,
            'created_at': None}
  

    # STARTUP CONNECTION TO ADAFRUIT IO Feeds

    # temperature
    temperature = create_feed_connection(aio, TEMERATURE_FEED)
    
    # humidity
    humidity = create_feed_connection(aio, HUMIDITY_FEED)

    # pressure
    pressure = create_feed_connection(aio, PRESSURE_FEED)

    # rainfall
    rainfall = create_feed_connection(aio, RAINFALL_FEED)

    # windspeed
    wind_speed = create_feed_connection(aio, WINDSPEED_FEED)

    # winddirection
    wind_direction = create_feed_connection(aio, WINDDIRECTION_FEED)

    # Air quality pm1.0
    aq_pm10 = create_feed_connection(aio, AIR_QUALITY_PM10)
    
    # Air quality pm2.5
    aq_pm25 = create_feed_connection(aio, AIR_QUALITY_PM25)

    # Air quality pm10.0
    aq_pm100 = create_feed_connection(aio, AIR_QUALITY_PM100)

    logging.info("[{}] Connection to Adafruit IO established".format(datetime.now()))

    # CREATE SCHEDULER
    scheduler = BackgroundScheduler()

    # Reset functions
    scheduler.add_job(reset_RG11, 'cron', hour=0)
    scheduler.add_job(reset_wind_speed, 'cron', hour=0)
    scheduler.add_job(reset_logs, 'cron', hour=0)
    scheduler.add_job(send_feed_data, 'cron', [aio, metadata,temperature, humidity, pressure, rainfall, wind_speed, wind_direction, aq_pm10, aq_pm25, aq_pm100], second=0)

    scheduler.start()

    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        while True:
            sleep(5)
    
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
        logging.error("Scheduled job failed, exiting with status code 1")
        sys.exit(1)

    

