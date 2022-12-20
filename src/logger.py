from contextvars import ContextVar
from logging import Formatter
import json
import uuid
import time


class PyTelemetryLogger:
    __context_trace_id = ContextVar('trace_id', default=None)
    __resource = {}


    @staticmethod
    def set_resource(service_name, service_version, service_environment):
        PyTelemetryLogger.__resource['service_name'] = service_name
        PyTelemetryLogger.__resource['service_version'] = service_version
        PyTelemetryLogger.__resource['service_environment'] = service_environment


    @staticmethod
    def get_resource():
        return PyTelemetryLogger.__resource


    @staticmethod
    def set_trace_id(trace_id):
        PyTelemetryLogger.__context_trace_id.set(trace_id)


    @staticmethod
    def get_trace_id():
        return PyTelemetryLogger.__context_trace_id.get()


class PyTelemetryContextFormatter(Formatter):

    LEVELS = {
        "TRACE": {
            "text": 'TRACE',
            "number": 1,
        },
        "DEBUG": {
            "text": 'DEBUG',
            "number": 5,
        },
        "INFO": {
            "text": 'INFO',
            "number": 9,
        },
        "WARN": {
            "text": 'WARN',
            "number": 13,
        },
        "ERROR": {
            "text": 'ERROR',
            "number": 17,
        },
        "FATAL": {
            "text": 'FATAL',
            "number": 21,
        },
    }

    def __init__(self):
        super(PyTelemetryContextFormatter, self).__init__()


    @classmethod
    def log_record_to_dict(cls, record):
        trace_id = PyTelemetryLogger.get_trace_id()

        if trace_id is None:
            trace_id = str(uuid.uuid4())
            PyTelemetryLogger.set_trace_id(trace_id)

        return ({
            "Timestamp": time.time_ns(),
            "TraceId": trace_id,
            "SeverityText": record.levelname,
            "SeverityNumber": PyTelemetryContextFormatter.LEVELS.get(record.levelname)['number'],
            "Body": record.msg,
            "Resource": PyTelemetryLogger.get_resource(),
            "InstrumentationScope": record.name,
            "Attributes": record.args
        })


    def format(self, record):
        return json.dumps(self.log_record_to_dict(record))
