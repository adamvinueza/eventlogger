'''
ADAPTED FROM state.py AT https://github.com/honeycombio/libhoney-py/
'''
import logging

CLIENT = None
WARNED_UNINITIALIZED = False

def warn_uninitialize():
    log = logging.getLogger()
    global WARNED_UNINITIALIZED
    if not WARNED_UNINITIALIZED:
        log.warn("global eventlogger method used before initialization")
        WARNED_UNINITIALIZED = True
