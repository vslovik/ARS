#!/usr/bin/env bash

echo "Beginning provisioning"
apt-get update

wget -qO- https://get.docker.com/ | sh