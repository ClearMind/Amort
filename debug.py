import logging

def error(src, msg):
    logger = logging.getLogger(src)
    logger.error(msg)

def debug(src, msg):
    logger = logging.getLogger(src)
    logger.debug(msg)