"""Configurations of gunicorn wsgi server."""

# bind
#
# Default: ['127.0.0.1:8000']
#
# The socket to bind.
from django.conf import settings

settings.configure()

bind = "0.0.0.0:5000"

# worker_class
##
# Default: 'sync'
#
# The type of workers to use.
#
# The default class (sync) should handle most “normal” types of workloads.
# You’ll want to read Design for information on when you might want to choose
# one of the other worker classes. Required libraries may be installed using
# setuptools’ extras_require feature.
#
# A string referring to one of the following bundled classes:
#
# - sync
# - eventlet - Requires eventlet >= 0.24.1 (or install it via pip install gunicorn[eventlet])
# - gevent - Requires gevent >= 1.4 (or install it via pip install gunicorn[gevent])
# - tornado - Requires tornado >= 0.2 (or install it via pip install gunicorn[tornado])
# - gthread - Python 2 requires the futures package to be installed
#   (or install it via pip install gunicorn[gthread])
worker_class = "gevent"

# workers
#
# Default: 1
#
# The number of worker processes for handling requests.
#
# A positive integer generally in the 2-4 x $(NUM_CORES) range.
# You’ll want to vary this a bit to find the best for your particular application’s work load.
#
# By default, the value of the WEB_CONCURRENCY environment variable, which is set by some
# Platform-as-a-Service providers such as Heroku. If it is not defined, the default is 1.
workers = 1

max_requests = 5000

# "timeout"
#
# Default: 30
#
# Workers silent for more than this many seconds are killed and restarted.
timeout = 30

# disable_redirect_access_to_syslog
#
# Default: False
#
# Disable redirect access logs to syslog.
disable_redirect_access_to_syslog = True

# loglevel
#
# Default: 'info'
#
# The granularity of Error log outputs.
#
# Valid level names are:
#
# - 'debug'
# - 'info'
# - 'warning'
# - 'error'
# - 'critical'
loglevel = "debug"
