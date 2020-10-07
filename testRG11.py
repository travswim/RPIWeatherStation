import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

count = 0
def button_callback(channel):
    global count
    count += 1
    print("Railfall: {:.2f}mm".format(count*0.02))

def RG11():

    import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
    # GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.add_event_detect(10, GPIO.RISING, callback=button_callback, bouncetime=115) # Setup event on pin 10 rising edge

    message = input("Press enter to quit\n\n") # Run until someone presses enter
    # return count
    GPIO.cleanup() # Clean up

def main():
    RG11()

if __name__ == '__main__':
    main()