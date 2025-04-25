#!/bin/sh
cd code

RUN_PORT=${PORT:-8000}
RUN_HOST=${HOST:-0.0.0.0}

gunicorn -k uvicorn.workers.UvicornWorker -b $RUN_HOST:$RUN_PORT --timeout 300 --log-level info --access-logfile - --error-logfile - main:app
