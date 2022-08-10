#!/bin/bash

export DC_IMAGE_TAG=$(date +%Y%m%d-%H%M)

sudo -E docker-compose -f docker-compose.build.yaml build
sudo -E docker-compose -f docker-compose.dev.yaml up