#!/bin/bash

alembic upgrade head \
&& uvicorn src.webserver.entrypoints.fastapi_app:app --host 0.0.0.0 --port 8000