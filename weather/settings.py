# settings.py

from dotenv import load_dotenv
import os
import socket

def get_env():
    """"
    Gets environment variables form .env file
    """
    try:
        load_dotenv(verbose=True)

        KEY = os.getenv("ADAFRUIT_IO_KEY")
        USERNAME = os.getenv("ADAFRUIT_IO_USERNAME")
        LATITUDE = os.getenv("LOCATION_LATITUDE")
        LONGITUDE = os.getenv("LOCATION_LONGITUDE")
        ELEVATION = os.getenv("LOCATION_ELEVATION")

        return KEY, USERNAME, LATITUDE, LONGITUDE, ELEVATION
    except OSError as ex:
        print(ex)

def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex)
        return False

if __name__ == "__main__":
    KEY, USERNAME, LATITUDE, LONGITUDE, ELEVATION = get_env()

    print("KEY =  {}".format(KEY))
    print("USERNAME =  {}".format(USERNAME))
    print("LATITUDE =  {}".format(LATITUDE))
    print("LONGITUDE =  {}".format(LONGITUDE))
    print("ELEVATION =  {}".format(ELEVATION))

    if not internet():
        raise ConnectionError("Cannot connect to internet")
        # TODO: log error
