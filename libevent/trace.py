import datetime
import libevent
import logging
import wrapt
import random
import traceback
from libevent.constants import SPAN_ID_BYTES, TRACE_ID_BYTES, APP_ID_KEY, ERROR_KEY
from typing import Any, Callable, Optional


@wrapt.decorator
def trace(wrapped: Callable, instance: Any, args, kwargs):
    tr = libevent.get_tracer()
    span = tr.start_span()
    span.event.add_field(libevent.constants.OPERATION_KEY, wrapped.__name__)
    if args:
        span.event.add_field(libevent.constants.ARGS_KEY, args)
    if kwargs and type(kwargs) is dict:
        span.event.add_field(libevent.constants.KWARGS_KEY, kwargs)
    result = None
    try:
        result = wrapped(*args, **kwargs)
        span.event.add_field(libevent.constants.RETURN_VALUE_KEY, result)
        return result
    except Exception:
        trace_info = traceback.format_exc()
        span.event.add_field(ERROR_KEY, trace_info)
        raise
    finally:
        tr.finish_span(span)


class Span(object):
    def __init__(self, trace_id: str, parent_id: str, event: libevent.Event,
                 is_root: bool = False):
        self.trace_id = trace_id
        self.parent_id = parent_id
        self.event = event
        self.event.start_time = datetime.datetime.now()
        self._is_root = is_root


class Trace(object):
    def __init__(self, trace_id: str):
        self.id = trace_id
        self.stack = []
        self.fields = {}


class Tracer(object):
    def __init__(self, auto: bool = True, debug: bool = False):
        """Creates a Tracer.
        Arguments:
            auto: bool    Initiate tracing upon creation.
            debug: bool   Enable logging at the DEBUG level.
        """
        self._client = libevent.state.CLIENT
        self._init_logger()
        self._trace = None
        self.debug = debug
        if auto:
            self.start_trace()

    def _init_logger(self):
        app_id = self._client[APP_ID_KEY]
        self._logger = logging.getLogger(app_id)
        self._logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)

    def log(self, msg: str, *args: Any, **kwargs: Any) -> None:
        if self.debug:
            self._logger.debug(msg, *args, **kwargs)

    def get_active_span(self):
        if self._trace:
            return self._trace.stack[-1]
        else:
            self.log("attempting to get an active span for a completed trace")
            return None

    def start_trace(self, trace_id: str = None,
                    parent_span_id: str = None) -> Span:
        if trace_id:
            self._trace = Trace(trace_id)
        else:
            self._trace = Trace(generate_trace_id())
        return self.start_span(parent_id=parent_span_id)

    def start_span(self, parent_id: str = None) -> Optional[Span]:
        """Creates a new span."""
        if not self._trace:
            return None
        span_id = generate_span_id()
        if parent_id:
            parent_span_id = parent_id
        else:
            if self._trace.stack:
                parent_span_id = self._trace.stack[-1].event.id
            else:
                parent_span_id = None
        evt = libevent.new_event(data=self._trace.fields, event_id=span_id)
        evt.add(data={
            'trace.traceId': self._trace.id,
            'trace.parentId': parent_span_id,
            'trace.spanId': span_id,
        })
        is_root = len(self._trace.stack) == 0
        span = Span(trace_id=self._trace.id, parent_id=parent_id, event=evt,
                    is_root=is_root)
        self._trace.stack.append(span)
        return span

    def finish_span(self, span: Span) -> None:
        if span is None:
            return
        if span.event:
            if self._trace:
                for k, v in self._trace.fields.items():
                    if k not in span.event.fields():
                        span.event.add_field(k, v)
            duration = datetime.datetime.now() - span.event.start_time
            duration_ms = duration.total_seconds() * 1000.0
            span.event.add_field('duration_ms', duration_ms)
            span.event.send()
            self._trace.stack.pop()

    def finish_trace(self, span: Span):
        self.finish_span(span)
        self._trace = None


def generate_span_id() -> str:
    format_str = "{{:0{:d}x}}".format(SPAN_ID_BYTES*2)
    sys_rand = random.SystemRandom()
    return format_str.format(sys_rand.getrandbits(SPAN_ID_BYTES*8))


def generate_trace_id() -> str:
    format_str = "{{:0{:d}x}}".format(TRACE_ID_BYTES*2)
    sys_rand = random.SystemRandom()
    return format_str.format(sys_rand.getrandbits(TRACE_ID_BYTES*8))
