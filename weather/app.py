# Dependencies
from time import sleep
import os
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import threading


# Sensor connections
from weather.sensors.RG11 import RG11, is_any_thread_alive, get_RG11, reset_RG11
from weather.sensors.i2c_devices import BME280
from weather.sensors.wind_speed import anemometer, get_wind_speed, reset_wind_speed
from weather.sensors.wind_direction import voltage, voltage_to_degrees, voltage_to_direction

# [x] TODO: Python app file/folder structure
# [ ] TODO: Logging - python
# [ ] TODO: Logging - GCP
# [x] TODO: Collect weather data
# [ ] TODO: Schedule every 15min
# [ ] TODO: Reset Rainfall counter
# [ ] TODO: Reset windspeed

def get_weather():
    # Get temperature, humidity, pressureasd
    temperature, humidity, pressure = BME280()
    print("\nTemperature: %0.1f C" % temperature)
    print("Humidity: %0.1f %%" % humidity)
    print("Pressure: %0.1f hPa" % pressure)

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
    
    """
    
    
    # Start monitoring rainfall from the RG11
    run_RG11 = threading.Thread(target=RG11, name="RG11", daemon=True)
    run_RG11.start()

    # Start monitoring the wind speed from the anemometer
    run_anemometer = threading.Thread(target=anemometer, name="Anemometer", daemon=True)
    run_anemometer.start()


    scheduler = BackgroundScheduler()
    
    scheduler.add_job(get_weather, 'cron', second=0)
    scheduler.add_job(get_weather, 'cron', second=10)
    scheduler.add_job(get_weather, 'cron', second=20)
    scheduler.add_job(get_weather, 'cron', second=30)
    scheduler.add_job(get_weather, 'cron', second=40)
    scheduler.add_job(get_weather, 'cron', second=50)
    
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            sleep(5)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown() 

    

    

# if __name__ == '__main__':
#     scheduler = BackgroundScheduler()