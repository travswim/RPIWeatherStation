
def voltage_to_direction(voltage: float) -> str:
    if voltage < 0.20625 or voltage > 3.09375:
        return "N"
    elif 0.20625 <= voltage < 0.61875:
        return "NE"

    elif 0.61875 <= voltage < 1.03125:
        return "E"

    elif 1.03125 <= voltage < 1.44375:
        return "SE"

    elif 1.44375 <= voltage < 1.85625:

def wind_direction():

    from time import sleep
    import busio
    import digitalio
    import board
    import adafruit_mcp3xxx.mcp3008 as MCP
    from adafruit_mcp3xxx.analog_in import AnalogIn
 
    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    
    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)
    
    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)
    
    # create an analog input channel on pin 0
    chan = AnalogIn(mcp, MCP.P0)
    while True:
        print('Raw ADC Value: ', chan.value)
        print('ADC Voltage: ' + str(chan.voltage) + 'V')
        print()
        sleep(2)
        

def main():
    wind_direction()

if __name__ == '__main__':
    main()