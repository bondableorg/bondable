#! /bin/sh
set -e

ddtrace-run gunicorn mysite.wsgi:application --config ./gunicorn_conf.py
