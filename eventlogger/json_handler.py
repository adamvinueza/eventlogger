def default(obj):
    try:
        return str(obj)
    except Exception:
        return 'eventlogger was unable to serialize value'
