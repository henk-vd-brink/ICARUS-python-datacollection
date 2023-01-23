#!/bin/bash

alembic upgrade head \
&& python3 -m gunicorn src.webserver.entrypoints.fastapi_app:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind unix:/tmp/gunicorn.sock \
    --log-level INFO \
    --access-logfile -
