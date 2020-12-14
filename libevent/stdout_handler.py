import sys
from typing import Any
from libevent.handler import Handler


class StdoutHandler(Handler):
    def send(self, evt: Any) -> None:
        print(evt, file=sys.stdout)
