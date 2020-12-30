from typing import Any
from libevent.fields import Fields


class Handler:
    fields: Fields
    def send(self, evt: Any) -> None: ...
