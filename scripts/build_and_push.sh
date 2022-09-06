#!/bin/bash

docker-compose -f docker-compose.ci.build.yaml build

while true; do
read -p "Do you want to proceed? (y/n) " yn

case $yn in
    [yY] ) break;;
    [nN] ) exit;;
    * ) echo "Invalid response, try again...";
esac
done

docker-compose -f docker-compose.ci.build.yaml push
