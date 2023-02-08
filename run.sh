#! /bin/sh
set -e

ddtrace-run gunicorn app:app --config ./gunicorn_conf.py
