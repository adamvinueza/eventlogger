"""
ADAPTED FROM state.py AT https://github.com/honeycombio/libhoney-py/
"""
from typing import Optional
import logging
import libevent.client

WARNED_UNINITIALIZED = False

CLIENT: Optional[libevent.client.Client] = None


def warn_uninitialized() -> None:
    logger = logging.getLogger()
    global WARNED_UNINITIALIZED
    if not WARNED_UNINITIALIZED:
        logger.warning("global libevent method used before initialization")
        WARNED_UNINITIALIZED = True
