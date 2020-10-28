from weather.sensors.i2c_devices import BME280, PM25
# from weather.sensors.wind_direction import voltage, voltage_to_degrees, voltage_to_direction
# from weather.sensors.wind_speed import button_callback, rotations
# from weather.sensors.RG11 import button_callback as bs, count

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
        
    

if __name__ == "__main__":
    unittest.main()