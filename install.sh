#!/bin/bash

# Install python and upgrade raspbian
sudo apt update && sudo apt upgrade -y
sudo apt install python3 -y
sudo apt install python3-pip -y

# Dependencies
pip3 install -r requirements.txt -y

# Run weather station app on restart
sudo cp weather.service /etc/systemd/system/weather.service
sudo reboot
