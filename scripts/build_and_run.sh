#!/bin/bash

export DC_IMAGE_TAG=$(date +%Y%m%d-%H%M)

docker-compose -f docker-compose.build.yaml build
docker-compose -f docker-compose.dev.yaml up