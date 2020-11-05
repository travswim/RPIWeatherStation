#!/bin/bash

sudo apt update && sudo apt upgrade -y

sudo apt install python3
sudo apt install python3-pip

pip3 install -r requirements.txt

nohup python3 -m weather &
