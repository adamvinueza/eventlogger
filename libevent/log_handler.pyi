import logging
from typing import Any, Optional
from libevent.handler import Handler


def default_logger(name: str = None,
                   level: int = logging.INFO) -> logging.Logger: ...


class LogHandler:
    def __init__(self,
                 logger: logging.Logger = default_logger()) -> None: ...
    @staticmethod
    def with_handler(name: Optional[str] = None,
                     handler: Any = logging.StreamHandler(),
                     level: int = logging.INFO) -> Handler: ...
    def send(self, evt: Any) -> None: ...
