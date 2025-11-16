import logging
import sys
from config import LOG_LEVEL, LOG_FILE

def setup_logging():
    log_format = "[%(asctime)s][%(levelname)s] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Настройка корневого логгера
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
    
    # Удаляем старые handlers
    logger.handlers.clear()
    
    # Handler для stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    logger.addHandler(console_handler)
    
    # Handler для файла (если LOG_FILE задан)
    if LOG_FILE:
        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter(log_format, date_format))
        logger.addHandler(file_handler)
    
    return logger

