import logging
from typing import Optional
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


class LogHandler(Handler):
    def __init__(self,
                 logger: Optional[logging.Logger] = None):
        if logger is None:
            logger = logging.getLogger()
        self.logger = logger

    @staticmethod
    def default_handler(name: str = None,
                        filename: str = None,
                        level: int = -1) -> Handler:
        if name:
            logger = logging.getLogger(name)
        else:
            logger = logging.getLogger()
        if level not in LOGLEVELS:
            level = logging.INFO
        logger.setLevel(level)
        if filename:
            lh = logging.FileHandler(filename)
            lh.setLevel(level)
            logger.addHandler(lh)
        return LogHandler(logger)

    @staticmethod
    def set_level(evt: Event, level: int) -> None:
        if level not in LOGLEVELS:
            evt.add_field(
                fields.ERROR,
                f"attempt to set unrecognized level: {level}"
            )
            level = logging.INFO
        evt.add_field(fields.LOG_LEVEL, level)

    def send(self, evt: Event) -> None:
        try:
            level = evt[fields.LOG_LEVEL]
            self.logger.log(level, str(evt))
        except KeyError:
            self.logger.log(logging.INFO, str(evt))
