from time import sleep
from datetime import datetime

# Global Vars
wind_speed = 0
max_wind_speed = float('-inf')
min_wind_speed = float('inf')

rotations = 0

def get_wind_speed() -> tuple:
    """
    Gets the current, maximum, and minimum windspeeds

    Arguments: None

    Returns: a tuple: (wind_speed, max_wind_speed, min_wind_speed)
    """
    global wind_speed
    global max_wind_speed
    global min_wind_speed
    
    return round(wind_speed,2), round(max_wind_speed, 2), round(min_wind_speed,2)

def reset_wind_speed() -> None:
    """
    Resets the maximum and minimum wind speeds

    Arguments: None

    Returns: None
    """
    global max_wind_speed
    global min_wind_speed

    max_wind_speed = float('-inf')
    min_wind_speed = float('inf')

def button_callback(channel) -> None:
    """
    Callback function to increase the number of rotations of the anemometer
    
    Arguments:
        - channel: the callback channel

    Returns: None
    """
    global rotations
    rotations += 1

def anemometer(avg_sampling_time: int = 60) -> None:
    """
    Calculates the anemometer wind speed

    Argumetns: None

    Retruns: None
    """
    import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
    # GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BCM) # Use physical pin numbering
    GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 8 to be an input pin and set initial value to be pulled low (off)
    # GPIO.add_event_detect(14, GPIO.FALLING, callback=button_callback, bouncetime=125)  
    GPIO.add_event_detect(14, GPIO.FALLING, callback=button_callback)


    # message = input("Press enter to quit\n\n") # Run until someone presses enter
    # return count
    while True:
        global rotations
        global max_wind_speed
        global min_wind_speed
        global wind_speed

        rotations = 0
        sleep(avg_sampling_time)
        wind_speed = round(rotations*2.25*1.609344/avg_sampling_time, 2)

        if wind_speed > max_wind_speed:
            max_wind_speed = wind_speed
        if wind_speed < min_wind_speed:
            min_wind_speed = wind_speed

        
    GPIO.cleanup() # Clean up

def is_any_thread_alive(threads) -> bool:
    """
    Checks if there are any threads running

    Arguments:
        - threads: A list of threads running

    returns: True if there are any live threads, False otherwise
    """
    return True in [t.is_alive() for t in threads]

def main() -> None:
    """
    Driver function
    """
    import threading
    run_anemometer = threading.Thread(target=anemometer, name="Anemometer", daemon=True)
    run_anemometer.start()
    # anemometer()
    while is_any_thread_alive([run_anemometer]):

        print("rotations: " + str(rotations) + "\t" + str(wind_speed) + "KPH" + "\t" + str(max_wind_speed) + "KPH" + "\t" + str(min_wind_speed) + "KPH")
        sleep(3)

if __name__ == '__main__':
    main()