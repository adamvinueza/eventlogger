"""
ADAPTED FROM state.py AT https://github.com/honeycombio/libhoney-py/
"""
from typing import Optional
import logging
import eventlogger.client

WARNED_UNINITIALIZED = False

CLIENT: Optional[eventlogger.client.Client] = None


def warn_uninitialized() -> None:
    log = logging.getLogger()
    global WARNED_UNINITIALIZED
    if not WARNED_UNINITIALIZED:
        log.warn("global eventlogger method used before initialization")
        WARNED_UNINITIALIZED = True
