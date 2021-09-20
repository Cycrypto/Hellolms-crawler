import os
import logging
import sqlite3
from pandas import read_sql

### BASIC CONSTANT ###
_DIR = os.path.abspath("../")

DB_NAME = "untitled"
DB_PATH = _DIR + "/" + DB_NAME+".db"

# CONN = sqlite3.connect(DB_PATH)
# CURSOR = CONN.cursor()
# _FILE = False
#
# if os.path.isfile(DB_PATH):
#     _FILE = True
#

DB_NAME = "test"
DB_PATH = _DIR + "/" + DB_NAME + ".db"

CONN = sqlite3.connect(DB_PATH)
CURSOR = CONN.cursor()
_FILE = False

if os.path.isfile(DB_PATH):
    _FILE = True


### LOGGER ###
_DEBUG = False
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(levelname)s] - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def _LOG(msgtype, sender, msg):

    if _DEBUG is False:     # 디버그모드가 켜져있는 경우만 로그 실행
        pass

    if _DEBUG is False:  # 디버그모드가 켜져있는 경우만 로그 실행
        pass


    else:
        if msgtype == 'debug':
            logger.setLevel(logging.DEBUG)
            logger.debug(f'from [{sender}], {msg}')

        elif msgtype == 'info':
            logger.setLevel(logging.INFO)
            logger.info(f'from [{sender}], {msg}')

        elif msgtype == 'warning':
            logger.setLevel(logging.WARNING)
            logger.warning(f'from [{sender}], {msg}')

        elif msgtype == 'error':
            logger.setLevel(logging.ERROR)
            logger.error(f'from [{sender}], {msg}')

        else:
            logger.setLevel(logging.WARNING)
            logger.warning(f'from [{sender}], MSGTYPE does not exist')
