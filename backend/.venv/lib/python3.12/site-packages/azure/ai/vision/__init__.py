# Copyright (c) Microsoft. All rights reserved.
# See https://aka.ms/azai/vision/license for the full license information.

"""
Azure AI Vision SDK for Python
"""

from .vision_base_client import *
from .image_analysis_client import *
from .diagnostics_logging import *

try:
    from .version import __version__
except ImportError:
    __version__ = '0.0.0'


from .properties import (
    PropertyCollection
)


from .enums import (
    ImageAnalysisErrorReason,
    ImageAnalysisResultReason,
    SessionStoppedReason,
    SessionStoppedErrorReason,
    SessionResultReason
)


# override __module__ for correct docs generation
root_namespace_classes = (
    ConsoleLogger,
    FileLogger,
    Frame,
    FrameFormat,
    FrameSource,
    FrameSourceCallback,
    FrameWriter,
    ImageAnalysisEventArgs,
    ImageAnalysisErrorDetails,
    ImageAnalysisOptions,
    ImageAnalysisResult,
    ImageAnalysisResultDetails,
    ImageAnalyzer,
    ImageSourceBuffer,
    ImageSourceBufferCallback,
    ImageWriter,
    MemoryLogger,
    VisionServiceOptions,
    VisionSource
)


for cls in root_namespace_classes:
    cls.__module__ = __name__
__all__ = [cls.__name__ for cls in root_namespace_classes]
