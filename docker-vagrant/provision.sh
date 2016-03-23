#!/usr/bin/env bash

echo "Buongiorno!"

sudo apt-get -y install python-setuptools python-dev build-essential
sudo easy_install pip
sudo pip install --upgrade virtualenv
sudo pip install --upgrade pip
sudo  pip install decorator
sudo  pip install python-dateutil