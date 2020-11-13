# Raspberry Pi Weather Station
The [Raspberry Pi](https://www.raspberrypi.org/) weather station is a small IoT project used to demonstrate the use of [Python](https://www.python.org/), Linux, [Adafruit IO](https://io.adafruit.com/), various meteorological sensors, and a Raspberry Pi to stream meteorological data. This guide provides the code installation and setup


## Background & Objectives
You can read about why I made this project here


## Bill of Materials and Tools
The excel spreadsheet contains all the materials, tools, and hardware used to assemble the weather station.
</br>
NOTE: Use the RG-15 for rainfall monitoring. The RG-11 was the only raing guage sensor available when I started this project. The RG-15 came out when I had already purchased the RG-11

## Wiring and Assembly
- separate pages
- fritzing

## Setup and Install
On your PC:
1. Download, install, and run [Raspberry Pi Imager](https://www.raspberrypi.org/downloads/) 
2. Choose `Raspberry Pi OS (Other)`
3. Choose the `Lite` version

1. Install git
```bash
sudo apt install git -y
```
2. Configure Raspberry -Pi
Use arrow keys, return, and tab to navigate/select
```bash
sudo raspi-config
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