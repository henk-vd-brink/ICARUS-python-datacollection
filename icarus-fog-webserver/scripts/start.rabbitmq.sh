#!/bin/bash

export USE_RABBITMQ_ENTRYPOINT=true
python3 -m src.webserver.entrypoints.rabbitmq_app