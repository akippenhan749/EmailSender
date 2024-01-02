"""A custom implementation of a logger."""

__author__ = "Adam Kippenhan"
__copyright__ = "Copyright 2024, Adam Kippenhan"
__maintainer__ = "Adam Kippenhan"
__license__ = "MIT"
__status__ = "Production"

from datetime import datetime
from inspect import getframeinfo, stack
from pathlib import Path
from typing import Union


class CustomLogger:
    """A custom class to perform logging."""

    def __init__(self, log_file: Union[Path, str] = "stdout"):
        """Initialize a CustomLogger object.

        Parameters
        ----------
        log_file : Union[Path, str], optional
            The file to log to. If a value of "stdout" is given (case
            insensitive), log messages will print to stdout. Defaults to
            "stdout".
        """
        self.log_file = log_file
        self.stdout = (
            True if type(log_file) is str and log_file.lower() == "stdout" else False
        )

    def error(self, message: str):
        """Write an error log message.

        Parameters
        ----------
        message : str
            The message to log.
        """
        frame_info = getframeinfo(stack()[1][0])
        output = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]} [ERROR {frame_info.function.replace('<module>', 'main')} {frame_info.lineno}] {message}\n"
        if self.stdout:
            print(output, end="")
        else:
            with open(self.log_file, "a+") as f:
                f.write(output)

    def info(self, message: str):
        """Write an info log message.

        Parameters
        ----------
        message : str
            The message to log.
        """
        frame_info = getframeinfo(stack()[1][0])
        output = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]} [INFO {frame_info.function.replace('<module>', 'main')} {frame_info.lineno}] {message}\n"
        if self.stdout:
            print(output, end="")
        else:
            with open(self.log_file, "a+") as f:
                f.write(output)

    def debug(self, message: str):
        """Write a debug log message.

        Parameters
        ----------
        message : str
            The message to log.
        """
        frame_info = getframeinfo(stack()[1][0])
        output = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]} [DEBUG {frame_info.function.replace('<module>', 'main')} {frame_info.lineno}] {message}\n"
        if self.stdout:
            print(output, end="")
        else:
            with open(self.log_file, "a+") as f:
                f.write(output)
