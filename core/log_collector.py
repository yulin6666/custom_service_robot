"""
日志收集器 - 用于捕获所有print输出
"""
import sys
from io import StringIO
from typing import List
from contextlib import contextmanager


class LogCollector:
    """收集程序运行过程中的所有输出"""

    def __init__(self):
        self.logs: List[str] = []
        self._original_stdout = None
        self._string_io = None

    def start_capture(self):
        """开始捕获输出"""
        self.logs = []
        self._original_stdout = sys.stdout
        self._string_io = StringIO()
        sys.stdout = self._string_io

    def stop_capture(self):
        """停止捕获并返回所有日志"""
        if self._original_stdout:
            sys.stdout = self._original_stdout
            output = self._string_io.getvalue()
            if output:
                self.logs.extend(output.split('\n'))
            self._string_io = None
            self._original_stdout = None
        return self.logs

    def get_logs(self) -> List[str]:
        """获取当前收集到的所有日志"""
        return self.logs

    def clear(self):
        """清空日志"""
        self.logs = []


@contextmanager
def capture_logs():
    """上下文管理器，用于捕获代码块中的所有输出"""
    collector = LogCollector()
    collector.start_capture()
    try:
        yield collector
    finally:
        collector.stop_capture()
