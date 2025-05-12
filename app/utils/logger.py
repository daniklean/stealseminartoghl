import logging
import sys
from config.settings import Config

def setup_logger(name):
    """Configura y devuelve un logger personalizado"""
    log_level = getattr(logging, Config.LOG_LEVEL)
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(f'{name.lower()}.log')
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
