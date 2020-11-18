from time import sleep
from datetime import datetime
import busio
import board
import sys

# [ ] TODO: VEML UV Sensor will be incorporated when houseing is available
# def VEML():
#     """
#     Gets the raw UV and level UV from the VEML6070

#     Arguments: None

#     Returns:
#         - raw UV intensity and index level as a tuple: (uv_raw, uv_levl)
#     """
#     import adafruit_veml6070
#     with busio.I2C(board.SCL, board.SDA) as i2c:
#         uv = adafruit_veml6070.VEML6070(i2c)
#         return uv.uv_raw, uv.get_index(uv.uv_raw)


def BME280() -> tuple:
    """
    Gets the temperature, humidity, and pressure from the BME280 sensor

    Arguments: None

    Returns:
        - temperature, humidity, pressure of the sensor as a tuple: (temperature, humidity, pressure)
    """
    import adafruit_bme280
    # Create library object using our Bus I2C ports
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
    except RuntimeError:
        sys.exit(1)
    return round(bme280.temperature,1), round(bme280.humidity, 2), round(bme280.pressure, 2)

# TODO: Implement PM2.5 Air Quality Sensor when wired
def PM25() -> tuple:
    """
    Gets the air quality for 1.0um, 2.5um, and 10.0um

    Arguments: None

    Returns:
        - pm 1.0, pm 2.5, pm 10.0
    """
    from digitalio import DigitalInOut, Direction, Pull
    import adafruit_pm25
    reset_pin = None

    

    try:
        # Create library object, use 'slow' 100KHz frequency!
        i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
        # Connect to a PM2.5 sensor over I2C
        pm25 = adafruit_pm25.PM25_I2C(i2c, reset_pin)
        aqdata = pm25.read()
        
    except RuntimeError:
       sys.exit(1)
    
    return aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"]

def main():
    """
    Driver function
    """
    while True:
        temperature, humidity, pressure = BME280()
        pm10, pm25, pm100 = PM25()
        # uv_raw, risk_level = VEML()
        print("\nTemperature: %0.1f C" % temperature)
        print("Humidity: %0.1f %%" % humidity)
        print("Pressure: %0.1f hPa" % pressure)
        # print("UV Reading: {0} | Risk Level: {1}".format(uv_raw, risk_level))
        print("Concentration Units (standard)")
        print("---------------------------------------")
        print(
            "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
            % (pm10, pm25, pm100)
        )

        
        sleep(2)

if __name__ == '__main__':
    main()
