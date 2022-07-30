#!/bin/bash

export DC_IMAGE_TAG=$(date +%Y%m%d-%H%M)

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

echo ""
echo "Pushed images to cloud with tag: "$DC_IMAGE_TAG
