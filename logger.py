import logging
import os
from logging.config import fileConfig

fileConfig(os.path.join(os.path.dirname(__file__), 'logger.ini'))
logger = logging.getLogger('root')
