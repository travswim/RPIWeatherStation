from weather.sensors.i2c_devices import BME280, PM25
from weather.sensors.wind_direction import voltage, voltage_to_degrees, voltage_to_direction
from weather.sensors.wind_speed import button_callback, rotations
from weather.sensors.RG11 import button_callback as bs, count
import RPi.GPIO as GPIO

import unittest

class Test_TestSensors(unittest.TestCase):
    def test_BME(self):
        temperature, humidity, pressure = BME280()
        self.assertIsNotNone(temperature)
        self.assertIsNotNone(humidity)
        self.assertIsNotNone(pressure)
    
    def testPM25(self):
        pm10, pm25, pm100 = PM25()
        self.assertIsNotNone(pm10)
        self.assertIsNotNone(pm25)
        self.assertIsNotNone(pm100)

    def test_wind_direction(self):
        chan = voltage()
        self.assertIsNotNone(voltage_to_direction(chan.voltage))
        self.assertIsNotNone(voltage_to_degrees(chan.voltage))

    def test_WindSpeed(self):
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(14, GPIO.FALLING, callback=button_callback)
        for i in range(3):
            self.assertIsNotNone(rotations)
            sleep(2)
        GPIO.cleanup()

    def test_rg11(self):
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(15, GPIO.FALLING, callback=bs) # Setup event on pin 10 rising edge
        
        for i in range(3):
            self.assertIsNotNone(count)
            sleep(2)

        GPIO.cleanup()
        
    



 
# Create library object using our Bus I2C port
# i2c = busio.I2C(board.SCL, board.SDA)
# bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
 
# OR create library object using our Bus SPI port
# spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
# bme_cs = digitalio.DigitalInOut(board.D10)
# bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, bme_cs)
 
# change this to match the location's pressure (hPa) at sea level
# bme280.sea_level_pressure = 1013.25
# 
# while True:
#     print("\nTemperature: %0.1f C" % bme280.temperature)
#     print("Humidity: %0.1f %%" % bme280.humidity)
#     print("Pressure: %0.1f hPa" % bme280.pressure)
#     print("Altitude = %0.2f meters" % bme280.altitude)
#     time.sleep(2)

# def BME():
#     import board
#     import busio
#     import adafruit_bme280
#     # Create library object using our Bus I2C ports
#     i2c = busio.I2C(board.SCL, board.SDA)
#     bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

#     return bme280.temperature, bme280.humidity, bme280.pressure

# def main():
#     while True:
#         temperature, humidity, pressure = BME()
#         print("\nTemperature: %0.1f C" % temperature)
#         print("Humidity: %0.1f %%" % humidity)
#         print("Pressure: %0.1f hPa" % pressure)
#         sleep(2)

# if __name__ == '__main__':
#     main()