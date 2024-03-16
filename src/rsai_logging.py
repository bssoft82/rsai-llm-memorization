import logging
from datetime import datetime
from config import Config as config

def initlogging(log_path):
    logging.basicConfig(
        filename=log_path,
        filemode='a',
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S%p',
        level=logging.INFO
    )
    logging.info('='*50)

def add_rsai_log(s):
    if config.get_print_to_console():
        print(s)
    logging.info(s)

def add_rsai_error(s):
    if config.get_print_to_console():
        print(s)
    logging.error(s)

