# Copyright (c) Microsoft. All rights reserved.
# See https://aka.ms/azai/vision/license for the full license information.

import ctypes

from .interop import _c_str, _call_hr_fn, _call_string_function_and_free, _call_bytes_fn, _spx_handle, _sdk_lib
from .enums import VisionOption


class PropertyCollection:
    """
    Class to get or set a property value from a property collection.
    """

    def __init__(self, handle: _spx_handle):
        self.__handle = handle

    def __del__(self):
        if _sdk_lib.ai_core_properties_handle_is_valid(self._handle):
            _sdk_lib.ai_core_properties_handle_release(self._handle)

    def get_property_by_id(self, property_id: VisionOption, default_value: str):
        """
        Returns value of a property.
        If the property value is not defined, the specified default value is returned.
        :param property_id: The id of the property.
        :param default_value: The default value which is returned if no value is defined for the property (empty string by default).
        :return: Value of the property.
        """
        c_name = _c_str(str(property_id))
        c_value = _c_str(default_value)
        c_id = ctypes.c_int(property_id.value)
        return _call_string_function_and_free(fn=_sdk_lib.ai_core_properties_string_get, *[self._handle, c_id, c_name, c_value])

    def set_property_by_id(self, property_id: VisionOption, value: str):
        """
        Set value of a property.
        :param property_id: The id of the property enum
        :param value: The value to set
        """
        c_name = _c_str(str(property_id))
        c_value = _c_str(value)
        c_id = ctypes.c_int(property_id.value)
        _call_hr_fn(fn=_sdk_lib.ai_core_properties_string_set, *[self._handle, c_id, c_name, c_value])

    def set_property(self, property_name: str, value: str):
        """
        Set value of a property.
        :param property_name: The id name of the property
        :param value: The value to set
        """
        c_name = _c_str(property_name)
        c_value = _c_str(value)
        _call_hr_fn(fn=_sdk_lib.ai_core_properties_string_set, *[self._handle, 0, c_name, c_value])

    def get_property(self, property_name: str, default_value: str = "") -> str:
        """
        Returns value of a property.
        If the property value is not defined, the specified default value is returned.
        :param property_name: The name of the property.
        :param default_value: The default value which is returned if no value is defined for the property (empty string by default).
        :return: Value of the property.
        """
        c_name = _c_str(property_name)
        c_value = _c_str(default_value)
        return _call_string_function_and_free(fn=_sdk_lib.ai_core_properties_string_get, *[self._handle, 0, c_name, c_value])

    def get_binary_data_property(self, property_name: str) -> bytes:
        """
        Returns a Python "bytes" object created from a native binary buffer.
        Note that data from the native buffer is copied while
        creating the "bytes" object, and the native buffer is freed.
        :param: The name of the property
        :return: A Python bytes object
        """
        c_name = _c_str(property_name)
        c_uint32_ptr_buffer_size = ctypes.POINTER(ctypes.c_uint32)()
        c_uint32_ptr_buffer_size.contents = ctypes.c_uint32(0)
        c_uint8_ptr_buffer = _call_bytes_fn(fn=_sdk_lib.ai_core_properties_binary_get,
                                            *[self._handle, 0, c_name, c_uint32_ptr_buffer_size])
        if c_uint32_ptr_buffer_size.contents.value > 0:
            bytes_buffer = bytes(c_uint8_ptr_buffer[:c_uint32_ptr_buffer_size.contents.value])
            _call_hr_fn(fn=_sdk_lib.ai_core_properties_binary_free, *[c_uint8_ptr_buffer])
            return bytes_buffer
        else:
            return bytes()

    @property
    def _handle(self) -> _spx_handle:
        return self.__handle
