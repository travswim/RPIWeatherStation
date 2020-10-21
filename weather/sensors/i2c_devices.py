from time import sleep
import busio
import board

# TODO: VEML UV Sensor will be incorporated when houseing is available
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


def BME280():
    """
    Gets the temperature, humidity, and pressure from the BME280 sensor

    Arguments: None

    Returns:
        - temperature, humidity, pressure of the sensor as a tuple: (temperature, humidity, pressure)
    """
    import adafruit_bme280
    # Create library object using our Bus I2C ports
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

    return bme280.temperature, bme280.humidity, bme280.pressure

# TODO: Implement PM2.5 Air Quality Sensor when wired
# def PM25():

def main():
    """
    Driver function
    """
    while True:
        temperature, humidity, pressure = BME280()
        # uv_raw, risk_level = VEML()
        print("\nTemperature: %0.1f C" % temperature)
        print("Humidity: %0.1f %%" % humidity)
        print("Pressure: %0.1f hPa" % pressure)
        # print("UV Reading: {0} | Risk Level: {1}".format(uv_raw, risk_level))
        sleep(2)

if __name__ == '__main__':
    main()