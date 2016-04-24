#!/usr/bin/env bash

echo "Beginning provisioning"
apt-get update

wget -qO- https://get.docker.com/ | sh

apt-get install -y apt-utils python-pip libpng-dev libfreetype6-dev libxft-dev python-matplotlib
apt-get install python-numpy
pip install networkx