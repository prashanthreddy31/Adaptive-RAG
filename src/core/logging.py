"""
Logger configuation module
"""

import logging
from src.core.config import Settings

def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        level=Settings.log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    return logging.getLogger(name)
