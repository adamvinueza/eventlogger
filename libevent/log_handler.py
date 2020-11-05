import logging
from typing import Any
import libevent.fields as fields
from libevent.event import Event
from libevent.handler import Handler

LOGLEVELS = [
    logging.DEBUG,
    logging.INFO,
    logging.WARNING,
    logging.ERROR,
    logging.CRITICAL
]


def default_logger(name: str = None,
                   level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


class LogHandler(Handler):
    def __init__(self,
                 logger: logging.Logger = default_logger()):
        self.logger = logger

    @staticmethod
    def with_handler(name: str = None,
                     handler: Any = logging.StreamHandler(),
                     level: int = logging.INFO) -> Handler:
        logger = logging.getLogger(name)
        logger.setLevel(level)
        handler.setLevel(level)
        logger.addHandler(handler)
        return LogHandler(logger)

    def send(self, evt: Event) -> None:
        try:
            level = evt[fields.LOG_LEVEL]
        except KeyError:
            level = self.logger.level
        self.logger.log(level, str(evt))
