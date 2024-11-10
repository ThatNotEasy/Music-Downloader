import logging, coloredlogs, os

def setup_logging():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Set up the logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    coloredlogs.install(level='INFO', fmt=log_format, logger=logger)
    file_handler = logging.FileHandler('logs/logs.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)
    
    return logger