import os
from datetime import datetime

from loguru import logger

CURRENT_DATE = datetime.utcnow().strftime("%Y-%m-%d")
CURRENT_PATH = os.path.abspath(__file__)
PARENT_PATH = os.path.dirname(CURRENT_PATH)
LOG_FOLDER_PATH = os.path.join(PARENT_PATH, "logs_storage")
LOG_PATH = os.path.join(LOG_FOLDER_PATH, f"{CURRENT_DATE}_log_info.log")


class Logger:
    __LOG_LEVELS = {
        "debug": logger.debug,
        "info": logger.info,
        "warning": logger.warning,
        "error": logger.error,
        "critical": logger.critical,
    }

    def __init__(self, level: str, msg: str):
        self._level = self.__LOG_LEVELS.get(level.lower())
        self._msg = msg
        logger.add(sink=LOG_PATH, backtrace=True, format="{time} {level} {message}")

    def create_log(self):
        self._level(self._msg)
        logger.add(sink=LOG_PATH, backtrace=True, format="{time} {level} {message}")
