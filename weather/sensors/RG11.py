import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep
import logging
from datetime import datetime
count = 0

def get_RG11() -> float:
    """
    Gets the amount of rainfall since the last reset

    Arguments: None

    Returns: The amount of water fallen in mm
    """
    logging.info("[{}] Got RG11 data".format(datetime.now()))
    return round(count*0.2, 2)

def reset_RG11():
    """
    Resets the counter

    Arguments: None

    Returns: None
    """
    global count
    count = 0
    logging.info("[{}] Reset RG11".format(datetime.now()))

def button_callback(channel):
    """
    Callback function to increase the rainfall counter for the RG11
    
    Arguments:
        - channel: the callback channel

    Returns: None
    """
    global count
    count += 1


def RG11():
    # import board
    # import busio
    import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
    # GPIO.I2C()
    # GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BCM)
    # GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    # GPIO.add_event_detect(15, GPIO.FALLING, callback=button_callback, bouncetime=115) # Setup event on pin 10 rising edge - Debounce set for internal testing
    GPIO.add_event_detect(15, GPIO.FALLING, callback=button_callback) # Setup event on pin 10 rising edge
    
    while True:
        sleep(3)

    GPIO.cleanup()


def is_any_thread_alive(threads):
    """
    Checks if there are any threads running

    Arguments:
        - threads: A list of threads running

    returns: True if there are any live threads, False otherwise
    """
    return True in [t.is_alive() for t in threads]

def main():
    """
    Driver function
    """
    import threading
    run_RG11 = threading.Thread(target=RG11, name="RG11", daemon=True)
    run_RG11.start()
    
    while is_any_thread_alive([run_RG11]):
        print("Rainfall: " + str(get_RG11()) + "mm")
        sleep(3)

if __name__ == '__main__':
    main()