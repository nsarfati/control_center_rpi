#!/bin/bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y python3-dev python3-pip libjpeg-dev libtiff5
cd py-spidev
make
sudo make install
pip3 install --no-cache-dir -r requirements.txt
