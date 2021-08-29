import os
import logging

_DIR = os.path.abspath(os.path.dirname(__file__))

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(levelname)s] - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def _LOG(msgtype, sender, msg):
    if msgtype == 'debug':
        logger.setLevel(logging.DEBUG)
        logger.debug(f'from{sender}, {msg}')

    elif msgtype == 'info':
        logger.setLevel(logging.INFO)
        logger.info(f'from{sender}, {msg}')

    elif msgtype == 'warning':
        logger.setLevel(logging.WARNING)
        logger.warning(f'from{sender}, {msg}')

    elif msgtype == 'error':
        logger.setLevel(logging.ERROR)
        logger.error(f'from{sender}, {msg}')

    else:
        logger.setLevel(logging.WARNING)
        logger.warning(f'from{sender}, MSGTYPE does not exist')