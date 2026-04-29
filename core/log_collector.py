"""
Log collector - captures all print output
"""
import sys
from io import StringIO
from typing import List
from contextlib import contextmanager


class LogCollector:
    """Collect all output during program execution"""

    def __init__(self):
        self.logs: List[str] = []
        self._original_stdout = None
        self._string_io = None

    def start_capture(self):
        """Start capturing output"""
        self.logs = []
        self._original_stdout = sys.stdout
        self._string_io = StringIO()
        sys.stdout = self._string_io

    def stop_capture(self):
        """Stop capturing and return all logs"""
        if self._original_stdout:
            sys.stdout = self._original_stdout
            output = self._string_io.getvalue()
            if output:
                self.logs.extend(output.split('\n'))
            self._string_io = None
            self._original_stdout = None
        return self.logs

    def get_logs(self) -> List[str]:
        """Get all currently collected logs"""
        return self.logs

    def clear(self):
        """Clear logs"""
        self.logs = []


@contextmanager
def capture_logs():
    """Context manager for capturing all output within a code block"""
    collector = LogCollector()
    collector.start_capture()
    try:
        yield collector
    finally:
        collector.stop_capture()
