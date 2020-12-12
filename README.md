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

## Tracing

Tracing is the monitoring or profiling of an application's execution. When we
trace an application's execution, we insert code logging relevant info, such
as what function is being executed, what its parameters are, when it began or
finished, whether errors occurred, etc.

`libevent` supports basic tracing via a global `Tracer` object. To trace an
application, put a call to `libevent.get_tracer` at the start of any
instrumentation. If you begin instrumentation at the entry point of your
application, tracing will continue throughout all instrumented calls until the
application exits or the trace is explicitly finished.

Here is a sample of tracing inside an AWS Lambda function:

```python

import boto3
import libevent
import inspect

lmb = boto3.client('lambda')

def handler(event, context):
    t = libevent.get_tracer(auto=False)
    span = t.get_active_span()
    span.add_field('operation', inspect.stack()[1][3])
    if type(event) is dict:
        span.event.add(event)
    else:
        span.event.add_field('event', str(event))
    with span.event.timer():
        resp = lmb.get_account_settings()
    span.event.add_field('response', resp)
    t.finish_trace(span=span)
    return resp
```

## Automatic Tracing

If you want minimal instrumentation in your code, you can use decorators for
tracing automatically. Using the `@trace` decorator, the function name and
parameters will be recorded, along with the function's entry and exit times
as well as the duration, and error information if an error occurred.
```python
import boto3
from libevent.trace import trace

lmb = boto3.client('lambda')

@trace
def handler(event, context):
    resp = lmb.get_account_settings()
    return resp
```