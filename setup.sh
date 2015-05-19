#!/usr/bin/env bash

# Init 
FILE="/tmp/out.$$" 
GREP="/bin/grep" 
#.... 
# Make sure only root can run our script 
if [ "$(id -u)" != "0" ]; then 
	echo "This script must be run as root" 1>&2 
	exit 1 
fi 
# ...

echo "Getting dependencies"

echo "installing pip3..."
sudo apt-get install python3-pip

echo "installing django"
sudo pip3 install django

echo "installing mysql..."
echo "mysql-server mysql-server/root_password password ruien9690" | debconf-set-selections
echo "mysql-server mysql-server/root_password_again password ruien9690" | debconf-set-selections
sudo apt-get install -y mysql-server

echo "installing dateutil..."
sudo apt-get install python3-dateutil

echo "installing markdown2..."
sudo pip3 install markdown2

echo "installing PyMySQL..."
sudo pip3 install PyMySQL

echo "installing FuzzyWuzzy..."
sudo apt-get install python-levenshtein
sudo pip3 install fuzzywuzzy

echo "installing Pillow..."
sudo apt-get install python3-dev python3-setuptools
sudo apt-get install libtiff4-dev libjpeg8-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev

sudo pip3 install Pillow
