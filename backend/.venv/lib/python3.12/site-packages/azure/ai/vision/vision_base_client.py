# Copyright (c) Microsoft. All rights reserved.
# See https://aka.ms/azai/vision/license for the full license information.
"""
Classes that handles vision base functionalities for the various recognizers/analyzers.
"""

import ctypes

from typing import Optional, Callable
from .properties import PropertyCollection
from .interop import (_CallbackContext, _Handle, _c_str, _call_hr_fn, _sdk_lib, _spx_handle, _call_bytes_fn, _trace_message,
                      _LogLevel, _unpack_context)
from .enums import SessionStoppedReason


class Frame():
    """
    Represents a Frame being passed into or retrieved from the Vision SDK.

    :param buffer:The memory that contains the frame.
    """

    def __init__(self, buffer: bytes, handle: Optional[_spx_handle] = None):
        # trace_message(LogLevel.Verbose, "Python:", "UKN", 0, "calling __init__")
        if handle is not None:
            frame_properties_handle = _spx_handle(0)
            _call_hr_fn(fn=_sdk_lib.vision_frame_properties_handle_get, *[handle, ctypes.byref(frame_properties_handle)])
            self.__properties = PropertyCollection(frame_properties_handle)
            c_size = ctypes.c_size_t(0)
            c_data_ptr = _call_bytes_fn(fn=_sdk_lib.vision_frame_get_data, *[handle, ctypes.byref(c_size)])
            if c_data_ptr is not None:
                self.__data = bytes(c_data_ptr[:c_size])
        else:
            core_properties_handle = _spx_handle(0)
            _call_hr_fn(fn=_sdk_lib.ai_core_properties_handle_create, *[ctypes.byref(core_properties_handle)])
            self.__properties = PropertyCollection(core_properties_handle)
            self.__data = buffer
        self.__handle = _Handle(handle, _sdk_lib.vision_frame_handle_is_valid, _sdk_lib.vision_frame_handle_release)

    @property
    def data(self) -> bytes:
        """
        The data buffer associated with the Frame.
        """
        return self.__data

    @property
    def properties(self) -> PropertyCollection:
        """
        A collection of properties and their values defined for this Frame.
        """
        return self.__properties

    @property
    def _handle(self):
        return self.__handle.get()

    def __str__(self):
        return f"Frame({type(self).__name__})"


class FrameWriter():
    """
    Represents the ability to write image frame data, for use as input with Vision AI scenario operations.
    """

    def __init__(self, handle: _spx_handle):
        self.__handle = _Handle(handle, _sdk_lib.vision_frame_writer_handle_is_valid, _sdk_lib.vision_frame_writer_handle_release)

    def write_bytes(self, buffer: bytes):
        """
        Writes a single frame of image data to the underlying FrameSource.

        :param buffer: The data buffer as bytes.
        """
        _call_hr_fn(fn=_sdk_lib.vision_frame_writer_write, *[self._handle, 0, buffer, len(buffer), None, None])

    def write_frame(self, frame: Frame):
        """
        Writes a single frame of image data to the underlying FrameSource.

        :param frame: The frame containing the data buffer.
        """
        if frame.data is None:
            raise ValueError('bad arguments: frame data is not valid')
        _call_hr_fn(fn=_sdk_lib.vision_frame_writer_write, *[self._handle, 0, frame.data, len(frame.data), None, None])

    @property
    def _handle(self):
        return self.__handle.get()

    def __str__(self):
        return f"FrameWriter({type(self).__name__})"


class FrameSourceCallback():
    """
    An interface that defines callback method used with FrameSource

    Not fully implemented.

    """

    def callback(self, frame_writer: FrameWriter) -> None:
        """
        This function is called by native side when new data is requested to be written using FrameWriter

        :param frame_writer: the frame writer object.
        """
        pass


class FrameFormat():
    """
    Represents a collection of image format properties (e.g. FOURCC, width, height, stride, ...)

    :param fourcc: Specifies the FOURCC character string.
    :param bits_per_pixel: The image format's bits per pixel (e.g. 8, 16, 24, 32, ...).
    :param width: The image format's pixel width.
    :param height: The image format's pixel height.
    :param stride: The image format's pixel stride.
    """

    def __init__(self, fourcc: str, bits_per_pixel: int = 0, width: int = 0, height: int = 0, stride: int = 0):
        if self.__is_fourcc_valid(fourcc) is False:
            raise ValueError('bad arguments: invalid fourcc format code')
        handle = _spx_handle(0)
        core_properties_handle = _spx_handle(0)
        _call_hr_fn(fn=_sdk_lib.ai_core_properties_handle_create, *[ctypes.byref(core_properties_handle)])
        core_properties = PropertyCollection(core_properties_handle)
        # TODO validity checks
        core_properties.set_property("frame.format.width", str(width))
        core_properties.set_property("frame.format.height", str(height))
        if stride > 0:
            core_properties.set_property("frame.format.stride", str(stride))
        # create list of python str characters
        fourcc_list = list(fourcc)
        # convert to list of c type char items
        chs = [ctypes.c_char(x.encode('utf-8')) for x in fourcc_list]
        if self.__is_rgb(fourcc) is True:
            core_properties.set_property("frame.format.bits.per.pixel", str(bits_per_pixel))
            _call_hr_fn(fn=_sdk_lib.vision_frame_format_handle_create, *[ctypes.byref(handle), chs[0], chs[1], chs[2], chs[3],
                        core_properties_handle])
        else:
            _call_hr_fn(fn=_sdk_lib.vision_frame_format_handle_create, *[ctypes.byref(handle), chs[0], chs[1], chs[2], chs[3],
                        core_properties_handle])

        frameformat_properties_handle = _spx_handle(0)
        _call_hr_fn(fn=_sdk_lib.vision_frame_format_properties_handle_get, *[handle, ctypes.byref(frameformat_properties_handle)])
        self.__properties = PropertyCollection(frameformat_properties_handle)
        self.__handle = _Handle(handle, _sdk_lib.vision_frame_format_handle_is_valid, _sdk_lib.vision_frame_format_handle_release)

    @property
    def fourcc(self) -> str:
        """
        Gets the image format's FOURCC value
        """
        fourcc = self.properties.get_property("frame.format.fourcc")
        return fourcc

    @property
    def width(self) -> int:
        """
        Gets the image format's pixel width.
        """
        width = self.properties.get_property("frame.format.width")
        return int(width)

    @property
    def height(self) -> int:
        """
        Gets the image format's pixel height.
        """
        height = self.properties.get_property("frame.format.height")
        return int(height)

    @property
    def stride(self) -> int:
        """
        Gets the image format's pixel stride.
        """
        stride = self.properties.get_property("frame.format.stride")
        if not stride:
            return 0
        else:
            return int(stride)

    @property
    def bits_per_pixel(self) -> int:
        """
        Gets the image format's bits per pixel value.
        """
        bits_per_pixel = self.properties.get_property("frame.format.bits.per.pixel")
        if not bits_per_pixel:
            return 0
        else:
            return int(bits_per_pixel)

    @property
    def properties(self) -> PropertyCollection:
        """
        A collection of properties and their values defined for this FrameFormat.
        """
        return self.__properties

    @property
    def _handle(self):
        return self.__handle.get()

    def __is_fourcc_valid(self, fourcc: str) -> bool:
        if len(fourcc) != 4:
            return False
        return True

    def __is_rgb(self, fourcc: str) -> bool:
        if fourcc.strip() == 'RGB':
            return True
        return False

    def __str__(self):
        return f"FrameFormat({type(self).__name__})"


class FrameSource():
    """
    Represents a source of image frame data, used as input to or output from Vision AI operations.

    :param format: Specifies the frame format
    :param frame_callback: The object containing the callback function for the pulling the frame data
    """

    def __init__(self, format: FrameFormat, frame_callback: Optional[FrameSourceCallback] = None):
        handle = _spx_handle(0)
        if frame_callback is None:
            _call_hr_fn(fn=_sdk_lib.vision_frame_source_handle_create, *[ctypes.byref(handle), _c_str("adapter.streams.count"),
                        _c_str("1"), format._handle, _c_str("adapter.streams.0.")])
        else:
            _call_hr_fn(fn=_sdk_lib.vision_frame_source_handle_create, *[ctypes.byref(handle), _c_str("adapter.streams.count"),
                        _c_str("1"), format._handle, _c_str("adapter.streams.0.")])
            self.__callback = frame_callback
            self.__context = _CallbackContext(self.__callback)
            context_ptr = ctypes.py_object(self.__context)
            _call_hr_fn(fn=_sdk_lib.vision_frame_source_callback_set, *[handle, context_ptr, FrameSource.__callback])

        propbag_handle = _spx_handle(0)
        _call_hr_fn(fn=_sdk_lib.vision_frame_source_properties_handle_get, *[handle, ctypes.byref(propbag_handle)])
        self.__properties = PropertyCollection(propbag_handle)
        writer_handle = _spx_handle(0)
        _call_hr_fn(fn=_sdk_lib.vision_frame_source_writer_handle_get, *[handle, ctypes.byref(writer_handle)])
        # TODO binding FrameSource and FrameWriter
        self.__frame_writer = FrameWriter(writer_handle)
        self.__handle = _Handle(handle, _sdk_lib.vision_frame_source_handle_is_valid, _sdk_lib.vision_frame_source_handle_release)

    def close(self) -> None:
        """
        Closes the frame source for writing.
        """
        _call_hr_fn(fn=_sdk_lib.vision_frame_source_close_writer, *[self._handle])

    @ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)
    def __callback(handle: ctypes.c_void_p, context: ctypes.c_void_p):
        obj = _unpack_context(context)
        if obj is not None:
            writer = FrameWriter(handle)
            obj.callback(writer)

    @property
    def frame_writer(self) -> FrameWriter:
        return self.__frame_writer

    @property
    def properties(self) -> PropertyCollection:
        """
        A collection of properties and their values defined for this FrameSource.
        """
        return self.__properties

    @property
    def _handle(self) -> _spx_handle:
        return self.__handle.get()


class ImageWriter():
    """
    Represents the ability to write image data, for use as input to Vision AI operations.
    """

    def __init__(self, handle: _spx_handle):
        self.__handle = _Handle(handle, _sdk_lib.vision_frame_writer_handle_is_valid, _sdk_lib.vision_frame_writer_handle_release)

    def write(self, buffer: bytes):
        """
        Writes a single image to the internal buffer.

        .. note::
          When used with ImageAnalyzer, the image needs to be in a format that's supported by the Image Analysis service,
          such as JPEG, PNG or BMP. See full list of supported formats here: https://aka.ms/ia-input.
          The SDK sends the image buffer as-is to the service. It does not do any format conversion or other modifications.

        :param buffer: The image buffer as a bytes object.
        """
        if buffer is None or buffer.__len__() == 0:
            raise ValueError('bad argument: invalid input buffer')
        _call_hr_fn(fn=_sdk_lib.vision_frame_writer_write, *[self._handle, 0, buffer, len(buffer), None, None])

    @property
    def _handle(self):
        return self.__handle.get()

    def __str__(self):
        return f"ImageWriter({type(self).__name__})"


class ImageSourceBufferCallback():
    """
    An interface that defines callback method used with ImageSourceBuffer.

    Not implemented.

    """

    def callback(self, image_writer: ImageWriter) -> None:
        """
        This function is called by native side when new data is requested to be written using ImageWriter

        :param image_writer: the image writer object.
        """
        pass


class ImageSourceBuffer():
    """
    Represents a source of image data, used as input to or output from Vision AI operations.

    .. note::
      When used with ImageAnalyzer, callback is not supported. Call this constructor without arguments.
      Then, using the image_writer property, get access to the ImageWriter object and write the image data to it.

    :param image_callback: An optional callback function that will be invoked when a new image is needed.
    """

    def __init__(self, image_callback: Optional[ImageSourceBufferCallback] = None):
        handle = _spx_handle(0)
        if image_callback is None:
            _call_hr_fn(fn=_sdk_lib.vision_frame_source_handle_create, *[ctypes.byref(handle), _c_str("adapter.streams.count"),
                        _c_str("1"), None, _c_str("adapter.streams.0.")])
        else:
            _call_hr_fn(fn=_sdk_lib.vision_frame_source_handle_create, *[ctypes.byref(handle), _c_str("adapter.streams.count"),
                        _c_str("1"), None, _c_str("adapter.streams.0.")])
            self.__callback = image_callback
            self.__context = _CallbackContext(self.__callback)
            context_ptr = ctypes.py_object(self.__context)
            _call_hr_fn(fn=_sdk_lib.vision_frame_source_callback_set, *[handle, context_ptr, ImageSourceBuffer.__callback])

        writer_handle = _spx_handle(0)
        _call_hr_fn(fn=_sdk_lib.vision_frame_source_writer_handle_get, *[handle, ctypes.byref(writer_handle)])
        # TODO binding ImageSourceBuffer and ImageWriter
        self.__image_writer = ImageWriter(writer_handle)
        self.__handle = _Handle(handle, _sdk_lib.vision_frame_source_handle_is_valid, _sdk_lib.vision_frame_source_handle_release)

    def close(self) -> None:
        """
        Closes the image source buffer for writing.
        """
        _call_hr_fn(fn=_sdk_lib.vision_frame_source_close_writer, *[self._handle])

    @ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)
    def __callback(handle: ctypes.c_void_p, context: ctypes.c_void_p):
        obj = _unpack_context(context)
        if obj is not None:
            writer = ImageWriter(handle)
            obj.callback(writer)

    @property
    def image_writer(self) -> ImageWriter:
        return self.__image_writer

    @property
    def _handle(self) -> _spx_handle:
        return self.__handle.get()


class VisionSource():
    """
    Represents a source of vision data, used as input to a Computer Vision operation.

    :param filename: Specifies the locally accessible image or video file.
    :param url: Specifies a publicly accessible image or video URL.
    :param image_source_buffer: Specifies a source image buffer.
    :param frame_source: Specifies a frame source.
    :param device_attributes: A string that specifies the attributes of the device (e.g. "front=true;", ...).
    """

    def __init__(self, filename: Optional[str] = None, url: Optional[str] = None,
                 image_source_buffer: Optional[ImageSourceBuffer] = None,
                 frame_source: Optional[FrameSource] = None, device_attributes: Optional[str] = None):
        handle = _spx_handle(0)
        if device_attributes is None and filename is None and url is None and frame_source is None and image_source_buffer is None:
            _call_hr_fn(fn=_sdk_lib.vision_source_handle_create, *[ctypes.byref(handle), _c_str("source.device.attributes"),
                        _c_str(""), None, None])
        else:
            if sum(x is not None for x in (device_attributes, filename, url, image_source_buffer, frame_source)) > 1:
                raise ValueError('bad arguments: only one of the device_attributes, filename, url, \
image_source_buffer and frame_source can be given')
            if device_attributes is not None:
                c_device_attributes = _c_str(device_attributes)
                _call_hr_fn(fn=_sdk_lib.vision_source_handle_create, *[ctypes.byref(handle), _c_str("source.device.attributes"),
                            c_device_attributes, None, None])
            elif filename is not None:
                c_filename = _c_str(filename)
                _call_hr_fn(fn=_sdk_lib.vision_source_handle_create, *[ctypes.byref(handle), _c_str("source.file.name"), c_filename,
                            None, None])
            elif url is not None:
                c_url = _c_str(url)
                _call_hr_fn(fn=_sdk_lib.vision_source_handle_create, *[ctypes.byref(handle), _c_str("source.url.name"), c_url, None,
                            None])
            elif frame_source is not None:
                _call_hr_fn(fn=_sdk_lib.vision_source_handle_create, *[ctypes.byref(handle), None, None,
                                                                       frame_source._handle, None])
            elif image_source_buffer is not None:
                _call_hr_fn(fn=_sdk_lib.vision_source_handle_create, *[ctypes.byref(handle), None, None,
                                                                       image_source_buffer._handle, None])
            else:
                raise ValueError('cannot construct VisionSource with the given arguments')
        propbag_handle = _spx_handle(0)
        _call_hr_fn(fn=_sdk_lib.vision_source_properties_handle_get, *[handle, ctypes.byref(propbag_handle)])
        self.__properties = PropertyCollection(propbag_handle)
        self.__handle = _Handle(handle, _sdk_lib.vision_source_handle_is_valid, _sdk_lib.vision_source_handle_release)

    @property
    def properties(self) -> PropertyCollection:
        """
        A collection of properties and their values defined for this VisionSource.
        """
        return self.__properties

    @property
    def _handle(self) -> _spx_handle:
        return self.__handle.get()


class VisionServiceAdvancedOptions():
    """
    Represents advanced options on the Vision Service.
    """
    def __init__(self):
        propbag_handle = _spx_handle(0)
        _call_hr_fn(fn=_sdk_lib.ai_core_properties_handle_create, *[ctypes.byref(propbag_handle)])
        self.__properties = PropertyCollection(propbag_handle)

    @property
    def properties(self) -> PropertyCollection:
        """
        A collection of properties and their values defined for this VisionServiceAdvancedOptions.
        """
        return self.__properties


class VisionServiceOptions():
    """
    Represents the configuration options used to connect to a remote Vision AI Service

    :param endpoint: The endpoint URL of the Vision Service
    :param key: The Computer Vision key used to authenticate against the Vision Service. Store your
    key securely. For example, using Azure Key Vault. Do not compile the value of your key into
    your application source code. Fetch it at run-time when needed from a secure location.
    """

    def __init__(self, endpoint: str, key: Optional[str] = None):
        propbag_handle = _spx_handle(0)
        _call_hr_fn(fn=_sdk_lib.ai_core_properties_handle_create, *[ctypes.byref(propbag_handle)])
        self.__advanced = VisionServiceAdvancedOptions()
        self.__advanced.properties.set_property("service.endpoint", str(endpoint))
        if key is not None:
            self.__advanced.properties.set_property("service.auth.key", str(key))

    @property
    def advanced(self) -> VisionServiceAdvancedOptions:
        """
        Advanced options for the Vision Service.
        """
        return self.__advanced

    @property
    def authorization_token(self) -> str:
        """
        The authorization token that will be used for connecting to the service.
        """
        return self.advanced.properties.get_property("service.auth.token")

    @authorization_token.setter
    def authorization_token(self, token: str):
        """
        Sets the authorization token to be used to connect to the service.
        If the previously given token has expired, you must set a new token before
        a new connections to the Vision Service can be made.

        :param token: The authorization token.
        """
        self.advanced.properties.set_property("service.auth.token", token)


class VisionSessionOptions():
    """
    Represents the options used to initialize a VisionSession instance.

    TBD: Define options setter properties

    """

    def __init__(self):
        core_properties_handle = _spx_handle(0)
        _call_hr_fn(fn=_sdk_lib.ai_core_properties_handle_create, *[ctypes.byref(core_properties_handle)])
        self.__properties = PropertyCollection(core_properties_handle)

    @property
    def properties(self) -> PropertyCollection:
        """
        A collection of properties and their values defined for this.
        """
        return self.__properties

    def __str__(self):
        return f"ImageAnalysisOptions({type(self).__name__})"


class VisionSession():
    """
    Represents the service configuration options and parameters used to connect to network attached
    AI inferencing technologies over IP based protocols.

    :param service_options: The vision service options.
    :param input: The vision source.
    :param options: The vision session options.
    """

    def __init__(self, service_options: VisionServiceOptions, input: VisionSource, options: Optional[VisionSessionOptions] = None):
        propbag_handle = _spx_handle(0)
        _call_hr_fn(fn=_sdk_lib.ai_core_properties_handle_create, *[ctypes.byref(propbag_handle)])
        self.__properties = PropertyCollection(propbag_handle)
        _call_hr_fn(fn=_sdk_lib.ai_core_properties_copy, *[service_options.advanced.properties._handle, propbag_handle, None])
        self.__properties.set_property("AZAC-SDK-PROGRAMMING-LANGUAGE", "python")
        # TODO combine also options parameter using ai_core_properties_copy
        handle = _spx_handle(0)
        _call_hr_fn(fn=_sdk_lib.vision_session_handle_create, *[ctypes.byref(handle), self.__properties._handle, input._handle])
        self.__handle = _Handle(handle, _sdk_lib.vision_session_handle_is_valid, _sdk_lib.vision_session_handle_release)

    @property
    def properties(self) -> PropertyCollection:
        """
        A collection of properties and their values defined for this VisionSource.
        """
        return self.__properties

    @property
    def session_id(self) -> str:
        """
        The authorization token that will be used for connecting to the service.
        """
        return self.properties.get_property("session.id")

    @property
    def _handle(self) -> _spx_handle:
        return self.__handle.get()

    def __str__(self):
        return f"VisionSession({type(self).__name__})"


class EventSignal():
    """
    Clients can connect to the event signal to receive events, or disconnect from
    the event signal to stop receiving events.
    """

    def __init__(self, obj, connection_changed_callback):
        """
        Constructor for internal use.
        """
        self.__connection_callback = connection_changed_callback
        self.__callbacks = list()
        self.__handle = obj._handle
        self.__context = _CallbackContext(obj)
        self.__context_ptr = None

    def __del__(self):
        self.disconnect_all()

    @property
    def _context_ptr(self):
        if self.is_connected():
            if self.__context_ptr is None:
                self.__context_ptr = ctypes.py_object(self.__context)
            return self.__context_ptr
        return None

    def connect(self, callback: Callable):
        """
        Connects given callback function to the event signal, to be invoked when the
        event is signalled.
        """
        self.__callbacks.append(callback)
        if len(self.__callbacks) == 1:
            self.__connection_callback(self, self.__handle)

    def disconnect_all(self):
        """
        Disconnects all registered callbacks.
        """
        empty = len(self.__callbacks) == 0
        self.__callbacks.clear()
        if not empty:
            self.__connection_callback(self, self.__handle)

    def signal(self, payload):
        for cb in self.__callbacks:
            try:
                cb(payload)
            except BaseException as e:
                _trace_message(_LogLevel.Error, "Callback raised exception", None, -1, f"Exception: {e}")

    def is_connected(self) -> bool:
        return len(self.__callbacks) > 0


class SessionStartedEventArgs():
    """
    Represents an event indicating vision session start.
    """

    def __init__(self, handle: _spx_handle):
        """
        Constructor for internal use.
        """
        self.__handle = _Handle(handle, _sdk_lib.vision_event_args_handle_is_valid, _sdk_lib.vision_event_args_handle_release)
        propbag_handle = _spx_handle(0)
        _call_hr_fn(fn=_sdk_lib.vision_event_args_properties_handle_get, *[self._handle, ctypes.byref(propbag_handle)])
        properties = PropertyCollection(propbag_handle)
        self.__session_id = properties.get_property("session.id", "")

    @property
    def _handle(self):
        return self.__handle.get()

    @property
    def session_id(self) -> str:
        """
        Gets the unique id for the Session from which this SessionResult originated.
        """
        return self.__session_id

    def __str__(self):
        return u'{}(session_id={})'.format(type(self).__name__, self.session_id)


class SessionStoppedEventArgs():
    """
    Represents an event indicating vision session stop.
    """

    def __init__(self, handle: _spx_handle):
        """
        Constructor for internal use.
        """
        self.__handle = _Handle(handle, _sdk_lib.vision_event_args_handle_is_valid, _sdk_lib.vision_event_args_handle_release)
        propbag_handle = _spx_handle(0)
        _call_hr_fn(fn=_sdk_lib.vision_event_args_properties_handle_get, *[self._handle, ctypes.byref(propbag_handle)])
        properties = PropertyCollection(propbag_handle)
        self.__session_id = properties.get_property("session.id", "")
        int_reason = int(properties.get_property("session.stopped.reason", "0"))
        self.__reason = SessionStoppedReason(int_reason)

    @property
    def _handle(self):
        return self.__handle.get()

    @property
    def session_id(self) -> str:
        """
        Gets the unique id for the Session from which this SessionResult originated.
        """
        return self.__session_id

    @property
    def reason(self) -> SessionStoppedReason:
        """
        Gets the SessionStoppedReason for generation of this result.
        """
        return self.__reason

    def __str__(self):
        return u'{}(session_id={})'.format(type(self).__name__, self.session_id)
