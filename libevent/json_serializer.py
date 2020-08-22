"""
ADAPTED FROM internal.py AT https://github.com/honeycombio/libhoney-py/
"""


# noinspection PyBroadException
def default(obj):
    try:
        return str(obj)
    except Exception:
        return 'libevent was unable to serialize value'
