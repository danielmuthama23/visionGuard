# Copyright (c) Microsoft. All rights reserved.
# See https://aka.ms/azai/vision/license for the full license information.
"""
Classes that handle Vision SDK logging for troubleshooting purposes. If you report an issue to Microsoft,
you may be asked to provide a Vision SDK log.
"""

import ctypes

from .properties import PropertyCollection
from .interop import (_c_str, _call_hr_fn, _call_fn, _call_size_t_fn, _call_string_function, _sdk_lib, _spx_handle)


class FileLogger():
    """
     Represents a process-wide singleton that emits SDK log traces to a provided file.
    """

    __properties = None

    @staticmethod
    def start(file_name: str, append: bool = False):
        """
        Starts logging to a file.

        :file_name: The name of the log file.
        :append: If set to True, and the log file already exists, new log messages will be appended
        to the existing file. Otherwise a new file will be created (this is the default).
        """
        if FileLogger.__properties is None:
            propbag_handle = _spx_handle(0)
            _call_hr_fn(fn=_sdk_lib.ai_core_properties_handle_create, *[ctypes.byref(propbag_handle)])
            FileLogger.__properties = PropertyCollection(propbag_handle)
        FileLogger.__properties.set_property("SPEECH-LogFilename", file_name)
        FileLogger.__properties.set_property("SPEECH-AppendToLogFile", "1" if append else "0")
        _call_hr_fn(fn=_sdk_lib.diagnostics_log_start_logging, *[FileLogger.__properties._handle, None])
        return

    @staticmethod
    def stop():
        """
        Stop logging to a file.
        """
        _call_hr_fn(fn=_sdk_lib.diagnostics_log_stop_logging)
        return


class ConsoleLogger():
    """
    Represents a process-wide singleton that emits SDK log traces to the console.
    """

    @staticmethod
    def start(log_to_stderr: bool = True):
        """
        Starts logging to the console.

        :append: If true, logs will be written to the standard error (STDERR) output. This is the
        default. Otherwise they will be written to the standard output (STDOUT).
        """
        _call_fn(fn=_sdk_lib.diagnostics_log_console_start_logging, *[log_to_stderr])
        return

    @staticmethod
    def stop():
        """
        Stop logging to a the console.
        """
        _call_fn(fn=_sdk_lib.diagnostics_log_console_stop_logging)
        return


class MemoryLogger():
    """
    Represents a process-wide singleton that stores SDK log messages in a memory buffer.
    """

    @staticmethod
    def start():
        """
        Starts logging to an internal buffer.
        """
        _call_fn(fn=_sdk_lib.diagnostics_log_memory_start_logging)
        return

    @staticmethod
    def stop():
        """
        Stop logging to an internal buffer.
        """
        _call_fn(fn=_sdk_lib.diagnostics_log_memory_stop_logging)
        return

    @staticmethod
    def dump_to_file(file_name: str):
        """
        Dumps the internal logging buffer to a given file.

        :file_name: Log file name.
        """
        c_file_name = _c_str(file_name)
        _call_hr_fn(fn=_sdk_lib.diagnostics_log_memory_dump, *[c_file_name, None, 0, 0])
        return

    # Note that we would have used the annotation `-> list[str]` below, however this is a Python 3.9 feature.
    # Since we run tests on 3.8 and up, we cannot use this annotation yet. But the functionality is the same.

    @staticmethod
    def dump_to_list() -> list:
        """
        Dumps the internal logging buffer to a list of strings.

        :file_name: Log file name.
        """
        list_log = []
        start = _call_size_t_fn(fn=_sdk_lib.diagnostics_log_memory_get_line_num_oldest)
        stop = _call_size_t_fn(fn=_sdk_lib.diagnostics_log_memory_get_line_num_newest)

        for i in range(start, stop):
            message = _call_string_function(fn=_sdk_lib.diagnostics_log_memory_get_line, *[i])
            list_log.append(message)

        return list_log
