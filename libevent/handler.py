from typing import Any, Protocol


class Handler(Protocol):

    def send(self, evt: Any) -> None:
        """Sends the supplied event.
        Strictly, anything can be an event. It is the responsibility of the
        event being sent to be appropriately serializable."""
        pass
