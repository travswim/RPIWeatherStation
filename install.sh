#!/bin/bash

# Install python and upgrade raspbian
sudo apt update && sudo apt upgrade -y
sudo apt install python3
sudo apt install python3-pip

# Dependencies
pip3 install -r requirements.txt

# Run weather station app on restart
sudo cp weather.service /etc/systemd/system/weather.service
sudo reboot
