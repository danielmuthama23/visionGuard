# Copyright (c) Microsoft. All rights reserved.
# See https://aka.ms/azai/vision/license for the full license information.

import ctypes
from enum import Enum
import os
import weakref


__load_library = ctypes.cdll
if os.name == 'nt':
    __library_name = "Azure-AI-Vision-Native.dll"
    __load_library = ctypes.windll
else:
    __library_name = "libAzure-AI-Vision-Native.so"
__lib_path = os.path.join(os.path.dirname(__file__), __library_name)
_sdk_lib = __load_library.LoadLibrary(__lib_path)
_spx_handle = ctypes.c_void_p
_spx_hr = ctypes.c_size_t
_spx_size_t = ctypes.c_size_t
_data_ptr = ctypes.POINTER(ctypes.c_uint8)
_max_uint32 = ctypes.c_uint32(((2 ** 32) - 1))


def _char_pointer_to_string(ptr: ctypes.POINTER(ctypes.c_char)):
    if ptr is None:
        return None
    c_ptr = ctypes.cast(ptr, ctypes.c_char_p)
    return c_ptr.value.decode(encoding='utf-8')


def __try_get_error(error_handle: _spx_handle):
    _sdk_lib.error_get_error_code.restype = _spx_hr
    code = _sdk_lib.error_get_error_code(error_handle)
    if code == 0:
        return
    _sdk_lib.error_get_call_stack.restype = ctypes.POINTER(ctypes.c_char)
    r_callstack = _sdk_lib.error_get_call_stack(error_handle)
    callstack = _char_pointer_to_string(r_callstack)
    _sdk_lib.error_get_message.restype = ctypes.POINTER(ctypes.c_char)
    r_what = _sdk_lib.error_get_message(error_handle)
    what = _char_pointer_to_string(r_what)
    message = "Exception with error code: %s%s" % (
        callstack if callstack is not None else "",
        what if what is not None else code
    )
    _sdk_lib.error_release(error_handle)
    raise RuntimeError(message)


def __raise_if_failed(hr: _spx_hr):
    if hr != 0:
        __try_get_error(_spx_handle(hr))
        raise RuntimeError(hr)


def _call_hr_fn(*args, fn):
    fn.restype = _spx_hr
    hr = fn(*args) if len(args) > 0 else fn()
    __raise_if_failed(hr)


def _call_size_t_fn(*args, fn):
    fn.restype = _spx_size_t
    size = fn(*args) if len(args) > 0 else fn()
    return size


def _call_string_function_and_free(*args, fn) -> str:
    fn.restype = ctypes.POINTER(ctypes.c_char)
    ptr = fn(*args) if len(args) > 0 else fn()
    if ptr is None:
        return None
    value = ctypes.cast(ptr, ctypes.c_char_p)
    string_value = value.value.decode(encoding='utf-8')
    _sdk_lib.ai_core_properties_string_free(ptr)
    return string_value


def _call_string_function(*args, fn) -> str:
    fn.restype = ctypes.POINTER(ctypes.c_char)
    ptr = fn(*args) if len(args) > 0 else fn()
    if ptr is None:
        return None
    value = ctypes.cast(ptr, ctypes.c_char_p)
    string_value = value.value.decode(encoding='utf-8')
    return string_value


def __call_bool_fn(*args, fn):
    fn.restype = ctypes.c_bool
    return fn(*args) if len(args) > 0 else fn()


def _call_fn(*args, fn):
    fn(*args) if len(args) > 0 else fn()


def _call_bytes_fn(*args, fn) -> ctypes.POINTER(ctypes.c_uint8):
    fn.restype = ctypes.POINTER(ctypes.c_uint8)
    ptr = fn(*args) if len(args) > 0 else fn()
    if ptr is None:
        return None
    return ptr


def _c_str(string: str) -> bytes:
    if string is None:
        return None
    return string.encode('utf-8')


def _release_if_valid(test_fn, release_fn, handle: _spx_handle):
    if __call_bool_fn(fn=test_fn, *[handle]):
        release_fn(handle)


class _Handle():
    def __init__(self, handle: _spx_handle, test_fn, release_fn):
        self.__handle = handle
        self.__test_fn = test_fn
        self.__release_fn = release_fn

    def __del__(self):
        if self.__test_fn is None:
            self.__release_fn(self.__handle)
        elif self.__test_fn(self.__handle):
            self.__release_fn(self.__handle)

    def get(self) -> _spx_handle:
        return self.__handle


class _CallbackContext():
    def __init__(self, obj):
        self.__obj = weakref.ref(obj)

    def get(self):
        return self.__obj()


def _unpack_context(context: ctypes.c_void_p):
    obj = ctypes.cast(context, ctypes.py_object).value
    return obj.get()


class _LogLevel(Enum):
    Error = 0x02
    Warning = 0x04
    Info = 0x08
    Verbose = 0x10


def _trace_message(level: _LogLevel, title: str, file: str, line: int, message: str):
    c_level = ctypes.c_int(level.value)
    c_title = _c_str(title)
    c_file = _c_str(file)
    c_line = ctypes.c_int(line)
    c_message = _c_str(message)
    _sdk_lib.diagnostics_log_trace_string(c_level, c_title, c_file, c_line, c_message)
