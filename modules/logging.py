import logging, coloredlogs

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    coloredlogs.install(level='DEBUG', fmt=log_format, logger=logger)
    return logger