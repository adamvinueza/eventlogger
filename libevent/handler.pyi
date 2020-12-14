from typing import Any


class Handler:
    def send(self, evt: Any) -> None: ...
