# import logging
# import os
# from logging.config import fileConfig

# fileConfig(os.path.join(os.path.dirname(__file__), 'logger.ini'))
# logger = logging.getLogger('root')
import logging

logging.basicConfig(filename='logs.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logging.info("Running Urban Planning")

logger = logging.getLogger('urbanGUI')