# libevent

A library for Writing events using handlers. By default, `libevent` uses a
simple `logging.Logger`, suitable for writing events to AWS CloudWatch.

`libevent` is a very, very streamlined version of Honeycomb's [`libhoney` Python
SDK](https://github.com/honeycombio/libhoney-py). I wrote it mostly as an
exercise to teach myself how to build an instrumentation library, but it may
come in handy for applications as well.

To accord with the `libhoney` license, the library source files have been
prominently documented as having been adapted from Honeycomb source files.

## Usage

## Sample

```python
#!/usr/bin/env python
import sys
import logging
import libevent

def get_line_count(file_path, call_id):
    """
    The call below creates an event with the following fields:
    {
        "timestamp": <current_time_in_iso_format>,
        "function": "get_line_count"
        "applicationId": "my_app",
        "parentId": "{call_id}",
        "eventId": <generated string identifier>
        "elapsedMs": <elapsed call time, in milliseconds>,
        "lineCount": <number of lines counted>
    }"""
    evt = libevent.new_event(calling_func=get_line_count, parent_id=call_id)
    evt.add_field("file_path", file_path)
    with evt.timer():
        """
        Times operations in this block and sets a field 
        with the elapsed time in milliseconds.
        """
        try:
            with open(file_path) as reader:
                line_count = sum(1 for line in reader)
                evt.add_field("lineCount", line_count)
        except Exception as e:
            evt.add_field("error", str(e))
    # By default, sends the serialized event to the default Python logger.
    evt.send()
    return line_count

if __name__ == '__main__':
    # By default, creates a handler that sends events as serialized JSON
    # to a logger that logs to stderr.
    libevent.init(app_id="my_app")
    evt = libevent.new_event()
    try:
        with evt.timer():
            file_of_interest = sys.argv[1]
            print(get_line_count(file_of_interest, evt.id))
    except IOError as err:
        evt.add_field(libevent.fields.ERROR, str(err))
    evt.send()
```
