import logging
from typing import Optional, Any
import libevent
import libevent.state as state
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
    def with_handler(name: str = None,
                     handler: Any = logging.StreamHandler,
                     level: int = logging.INFO) -> Handler:
        if not name and libevent.APP_ID_KEY in state.CLIENT:  # type: ignore
            name = state.CLIENT[libevent.APP_ID_KEY]  # type: ignore
        logger = logging.getLogger(name)
        logger.setLevel(level)
        handler.setLevel(level)
        logger.addHandler(handler)
        return LogHandler(logger)

    @staticmethod
    def default_handler(name: str = None,
                        filename: str = None,
                        level: int = logging.INFO) -> Handler:
        if filename:
            return LogHandler.with_handler(name,
                                           logging.FileHandler(filename),
                                           level)
        return LogHandler.with_handler(name, logging.StreamHandler(), level)

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
