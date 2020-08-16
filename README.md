# EventLogger

Logs events to the default logger. Suitable for use in applications monitored
via AWS Cloudwatch.

This library is a very, very streamlined version of Honeycomb's `libhoney`
Python SDK. I wrote it mostly as an exercise to teach myself how to build an
instrumentation library, but it may come in handy for applications as well.

To accord with the `libhoney` license, the library source files have been
prominently documented as having been adapted from Honeycomb source files.
