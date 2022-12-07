#!/bin/bash

uvicorn src.filesaver.entrypoints.fastapi_app:app --host 0.0.0.0 --port 8000