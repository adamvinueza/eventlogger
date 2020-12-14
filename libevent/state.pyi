from typing import Optional
import libevent

WARNED_UNINITIALIZED: bool
CLIENT: Optional[libevent.client.Client]


def warn_uninitialized() -> None: ...
