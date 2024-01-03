import logging
import json


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger_name": record.name,
            # "module": record.module,
            # "function": record.funcName,
            # "line_number": record.lineno,
        }
        return json.dumps(log_data)
