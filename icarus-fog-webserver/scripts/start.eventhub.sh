#!/bin/bash

sleep 5 \
&& alembic upgrade head \
&& python3 -m src.webserver.entrypoints.eventhub_app