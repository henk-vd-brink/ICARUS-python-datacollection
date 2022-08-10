#!/bin/bash

sudo -E docker-compose -f docker-compose.build.yaml build

while true; do
read -p "Do you want to proceed? (y/n) " yn

case $yn in
    [yY] ) break;;
    [nN] ) exit;;
    * ) echo "Invalid response, try again...";
esac
done

sudo -E docker-compose -f docker-compose.build.yaml push
