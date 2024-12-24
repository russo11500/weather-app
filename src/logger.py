import logging

from src.config import Config as config


logging.basicConfig(level=config.LOG_LEVEL, format='%(message)s')
logger = logging.getLogger(__name__)
