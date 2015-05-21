#!/usr/bin/env bash
echo "Getting dependencies"

echo "installing django"
sudo apt-get install python-django

echo "installing mysql..."
echo "mysql-server-5.5 mysql-server/root_password password ruien9690" | debconf-set-selections
echo "mysql-server-5.5 mysql-server/root_password_again password ruien9690" | debconf-set-selections
sudo apt-get install mysql-server

echo "installing dateutil..."
sudo apt-get install python3-dateutil

echo "installing pip3..."
sudo apt-get install python3-setuptools
sudo easy_install3 pip
echo "installing PyMySQL..."
sudo pip3 install PyMySQL

echo "installing FuzzyWuzzy..."
sudo apt-get install python-levenshtein
sudo pip3 install fuzzywuzzy
