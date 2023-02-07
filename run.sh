#! /bin/sh
set -e

alembic upgrade head
ddtrace-run gunicorn app:app --config ./gunicorn_conf.py
