import logging
from typing import Optional
import eventlogger.state as state
import eventlogger.fields as fields
from eventlogger.event import Event
from eventlogger.handler import Handler
from eventlogger.client import Client

LOGLEVELS = [
    logging.DEBUG,
    logging.INFO,
    logging.WARNING,
    logging.ERROR,
    logging.CRITICAL
]


class LogHandler(Handler):
    def __init__(self, client: Optional[Client] = None, logger: logging.Logger = None):
        if client is None:
            self.client = state.CLIENT
        if logger is None:
            logger = logging.getLogger()
        self.logger = logger

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
