# Raspberry Pi Weather Station
The [Raspberry Pi](https://www.raspberrypi.org/) weather station is an IoT project used to demonstrate the use of [Python](https://www.python.org/), Linux, [Adafruit IO](https://io.adafruit.com/), various meteorological sensors, and a Raspberry Pi to stream meteorological data. It uses Raspberry Pi OS (lite) and python to collect meteorological data and send it to Adafruit IO. This guide provides the code installation and setup.


## Background & Objectives
You can read about why I made this project here


## Bill of Materials and Tools
The excel spreadsheet contains all the materials, tools, and hardware used to assemble the weather station. Some updates are also provided here:
</br></br>
### UPDATE - Hydreon RG-15
When I first set out do buy a digital rain guage to replace a tipping bucket, the best option that stood out was the [Hydreon RG-11](https://rainsensors.com/products/rg-11/). Since completing this project, Hydreon has come out with a better version of their digital rain gauge called the [RG-15](https://rainsensors.com/products/rg-15/). Although being more expensive than the RG-11, it is specifically designed to be a digital solution to replace the tipping-bucket, and is more accurate (± 10%) than the RF-11 (± 36% 2/3 of the time).

## Wiring and Assembly
- separate pages
- fritzing

## Setup and Install
NOTE: This assumes you have correctly wired and installed your Raspberry Pi to the sensors.
### Setup Adafruit IO and your `.env` file
1. Create an [Adafruit](https://www.adafruit.com/) account
2. Login and Navigate to [Adafruit IO](https://io.adafruit.com/)
3. Using a text editior of your choice, create a file called `.env` and add the following information:
```
ADAFRUIT_IO_USERNAME = <"your_adafruit_io_username">
ADAFRUIT_IO_KEY = <"your_adafruit_io_key">

LOCATION_LATITUDE = <latitude_of weather station>
LOCATION_LONGITUDE = <longitude_of_weather_station>
LOCATION_ELEVATION = <elevation_of_weather_station>
```
Your username and key can be found under the `My Key` tab (hilighted in yellow)</br>
4. Save your `.env` file for later

### On your PC:
1. Insert your microSD card into your computer, and format it as FAT32 using [Windows](https://www.diskinternals.com/partition-recovery/format-sd-card-fat32-windows-10/), [macOS](https://www.easeus.com/mac-file-recovery/format-usb-flash-drive-to-fat32-on-mac.html), or [Linux](https://linuxhint.com/format_usb_drive_linux/). I would suggest using the disk utility method for both macOS and Linux if those options are available.
2. Download, install, and run [Raspberry Pi Imager](https://www.raspberrypi.org/downloads/) 
3. Under `Operating System` Choose `Raspberry Pi OS (Other)` --> `Raspberry Pi OS (Lite)`
4. Under `SD Card` choose the SD card that your formatted earlier in step `1`
5. Hit the `Write` Button and follow the onscreen instructions </br>
### The following instructions are to be used if you plan on setting up you Raspberry Pi completely headless. Otherwise the following steps can be setup using `raspi-config`
6. Once the Card has finished writing the OS image, remove and re-insert your SD card back into your computer
7. You need to add to files to the `boot` partition:</br></br>
    a. And empty file called `ssh` (no extension). This will allow remote ssh into the raspberry pi for configuration. See step [3. Enable SSH on a headless Raspberry Pi (add file to SD card on another machine)](https://www.raspberrypi.org/documentation/remote-access/ssh/)</br></br>
    b. If you plan on connection your Raspberry Pi through an RJ45 Ethernet cable you can skip this step. If the RaspberryPi will be connected using WIFI, modify `wpa-supplicant` file by adding your [WIFI SSID and passowrd by "Adding the network details to the Raspberry Pi"](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md)</br></br>
8. Eject the SD card from your computer. Insert it into the Raspberry Pi and power it on.


## On your Raspberry Pi (via SSH)
1. Install git
```bash
$ sudo apt install git -y
```
2. Configure Raspberry -Pi
Use arrow keys, return, and tab to navigate/select
```bash
$ sudo raspi-config
```
- env file
- raspi-config

# Troubleshooting
- Reset SPI and I2C if sensors stop working:
```bash
$ sudo raspi-config
```

- legal
- contributing guidelines
- wiki
- CI/CD
- finish testing