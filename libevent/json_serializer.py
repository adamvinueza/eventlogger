"""
ADAPTED FROM internal.py AT https://github.com/honeycombio/libhoney-py/
"""
import datetime


# noinspection PyBroadException
def default(obj):
    try:
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat() + 'Z'
        return str(obj)
    except Exception:
        return 'libevent was unable to serialize value'
