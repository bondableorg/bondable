#! /bin/sh
set -e

DD_GEVENT_PATCH_ALL=true ddtrace-run gunicorn api_crud.wsgi --workers 4 --bind :8000 --timeout 120
