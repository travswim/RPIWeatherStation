from time import sleep
from datetime import datetime
import sys

def voltage_to_direction(voltage: float) -> str:
    """
    Converts an anolog voltage to a direction

    Arguments:
        - voltage: Voltage float value form the MCP3008. values are between 0 and 3.3V

    Returns:
        - Direction coresponding to an input voltage
    """
    if voltage < 0.20625 or voltage > 3.09375:
        return "N"
    elif 0.20625 <= voltage < 0.61875:
        return "NE"

    elif 0.61875 <= voltage < 1.03125:
        return "E"

    elif 1.03125 <= voltage < 1.44375:
        return "SE"

    elif 1.44375 <= voltage < 1.85625:
        return "S"

    elif 1.85625 <= voltage < 2.26875:
        return "SW"

    elif 2.26875 <= voltage < 2.68125:
        return "W"

    else:
        return "NW"


def voltage_to_degrees(voltage: float) -> int:
    """
    Converts an anolog voltage to rotational degrees

    Arguments: None

    Returns:
        - Degrees coresponding to an input voltage
    """
    return int(voltage*360/3.3)


def voltage() -> float:
    """
    Gets the analog voltage from pin 0 on the MCP3008

    Arguments: None

    Returns:
        - The analog voltage
    """
    import busio
    import digitalio
    import board
    import adafruit_mcp3xxx.mcp3008 as MCP
    from adafruit_mcp3xxx.analog_in import AnalogIn
    
    try:
        # create the spi bus
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        
        # create the cs (chip select)
        cs = digitalio.DigitalInOut(board.D5)
        
        # create the mcp object
        mcp = MCP.MCP3008(spi, cs)
        
        # create an analog input channel on pin 0
        chan = AnalogIn(mcp, MCP.P0)
        
        return chan
    except:
        sys.exit(1)
    
        

def main():
    """
    Driver function
    """
    degree_sign= u'\N{DEGREE SIGN}'
    chan = voltage()
    while True:
        print('Raw ADC Value: ', chan.value)
        print('ADC Voltage: ' + str(chan.voltage) + 'V')
        print('Direction: ' + voltage_to_direction(chan.voltage))
        print('Direction: ' + str(voltage_to_degrees(chan.voltage)) + degree_sign)
        print()
        sleep(2)
    

if __name__ == '__main__':
    main()