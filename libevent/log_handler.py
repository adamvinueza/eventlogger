import logging
import sys
from typing import Any
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
    # log to stdout by default
    handler = logging.StreamHandler(sys.stdout)
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

    def send(self, evt: Any) -> None:
        """Sends the supplied event.
        Strictly, anything can be an event. It is the responsibility of the
        event being sent to be appropriately serializable."""
        self.logger.log(self.logger.level, str(evt))
