import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

rotations = 0
def button_callback(channel):
    global rotations
    rotations += 1
    print("Number of rotations: {0}".format(rotations))

def RG11():

    import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
    # GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 8 to be an input pin and set initial value to be pulled low (off)
    GPIO.add_event_detect(8, GPIO.RISING, callback=button_callback, bouncetime=115) # Setup event on pin 8 rising edge

    message = input("Press enter to quit\n\n") # Run until someone presses enter
    # return count
    GPIO.cleanup() # Clean up

def main():
    RG11()

if __name__ == '__main__':
    main()