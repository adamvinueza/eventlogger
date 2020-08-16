'''
ADAPTED FROM internal.py AT https://github.com/honeycombio/libhoney-py/
'''


def default(obj):
    try:
        return str(obj)
    except Exception:
        return 'eventlogger was unable to serialize value'
