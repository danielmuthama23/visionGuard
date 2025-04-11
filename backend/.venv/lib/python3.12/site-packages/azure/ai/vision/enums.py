# Copyright (c) Microsoft. All rights reserved.
# See https://aka.ms/azai/vision/license for the full license information.

from enum import Enum
from enum import Flag, auto


class VisionOption(Enum):
    """
    Defines the vision options base class. Not Implemented.
    """
    pass


class ImageSegmentationMode(Enum):
    """
    Defines the segmentation mode supported by the Image Analysis service.
    """

    NONE = 0
    """
    The default value. No segmentation is performed.
    """

    BACKGROUND_REMOVAL = 1
    """
    Background removal. Segmentation results in a PNG image of the detected
    foreground object with a transparent background.
    """

    FOREGROUND_MATTING = 2
    """
    Foreground matting. Segmentation results in a grayscale alpha matte PNG image
    showing the opacity of the detected foreground object.
    """


class ImageAnalysisFeature(Flag):
    """
    Defines the supported visual features to detect in an image.
    """

    TAGS = auto()
    """
    Tags the image with a detailed list of recognizable objects, living beings, scenery, and actions that appear in the image.
    The language of the tags can be specified by setting the property ImageAnalysisOptions.language
    """

    CAPTION = auto()
    """
    Generates a human-readable phrase that describes the image content, in one of the supported languages.
    Gender neutral caption can be requested by setting ImageAnalysisOptions.gender_neutral_caption to True.
    The language can be specified by setting the property ImageAnalysisOptions.language.
    """

    DENSE_CAPTIONS = auto()
    """
    Dense Captions provides more details than ImageAnalysisFeature.CAPTION, by generating one sentence
    descriptions of up to 10 regions of the image in addition to describing the whole image. Dense Captions
    also returns bounding box coordinates of the described image region.
    Gender neutral caption can be requested by setting ImageAnalysisOptions.gender_neutral_caption to True.
    The language can be specified by setting the property ImageAnalysisOptions.language.
    """

    OBJECTS = auto()
    """
    Detects various objects within an image, including their approximate location.
    Object names are only available in English at the moment.
    """

    PEOPLE = auto()
    """
    Detects people in the image, including their approximate location
    """

    TEXT = auto()
    """
    Also known as Read or OCR. Performs Optical Character Recognition (OCR)
    and returns the text detected in the image, including the approximate location
    of every text line and word.
    """

    CROP_SUGGESTIONS = auto()
    """
    Also known as SmartCrops. Returns recommendations for image crop operations that preserve content (for example
    for thumbnail generation).
    Provide requested aspect ratios by setting ImageAnalysisOptions.cropping_aspect_ratios
    """


class ImageAnalysisErrorReason(Enum):
    """
    A categorical representation of error classes that can cause an Image Analysis request to fail.
    """

    AUTHENTICATION_FAILURE = 1
    """
    Indicates an authentication error.
    An authentication error occurs if subscription key or authorization token is invalid, expired,
    or does not match the region being used.
    """

    BAD_REQUEST = 2
    """
    Indicates that one or more image analysis parameters are invalid or the image format is not supported.
    """

    TOO_MANY_REQUESTS = 3
    """
    Indicates that the number of parallel requests exceeded the number of allowed concurrent analysis
    operations for the subscription.
    """

    FORBIDDEN = 4
    """
    Indicates that the free subscription used by the request ran out of quota.
    """

    CONNECTION_FAILURE = 5
    """
    Indicates a connection error.
    """

    SERVICE_TIMEOUT = 6
    """
    Indicates a time-out error when waiting for response from the Computer Vision service.
    """

    SERVICE_ERROR = 7
    """
    Indicates an internal service error.
    """

    SERVICE_UNAVAILABLE = 8
    """
    Indicates that the service is currently unavailable.
    """

    RUNTIME_ERROR = 9
    """
    Indicates any other service errors.
    """


# Internal implementation note: ImageAnalysisResultReason *DOES NOT* map directly to the "result reason" enumerations in core, as
# here we merge the concept of stop reason and result reason together (as there's no "stop" for IA).


class ImageAnalysisResultReason(Enum):
    """
    Represents the reasons why an Image Analysis operation concluded.
    """

    ERROR = 1
    """
    Indicates that a result was generated due to an error during Image Analysis.
    More information about the error can be obtained by creating an ImageAnalysisErrorDetails object,
    by calling ImageAnalysisErrorDetails.from_result, and passing in the result.
    """

    ANALYZED = 2
    """
    Indicates that Image Analysis was successful and results are available.
    """


class _ImageAnalysisCoreResultReason(Enum):
    """
    Internal use only. A direct mapping of the core property "result.reason" enumeration into Python APIs.
    This is merged with the core "session.stopped.reason" for simplification in the public Image Analysis surface.
    """

    STOPPED = 1
    """
    Indicates the requested operation was stopped. Not supported at the moment.
    """

    ANALYZED = 2
    """
    Indicates that Image Analysis results are available.
    """


class _ImageAnalysisCoreStopReason(Enum):
    """
    Internal use only. Defines the reason why the session stopped.
    """

    ERROR = -1
    """An error occurred."""


class SessionStoppedReason(Enum):
    """
    Defines the reason why the session stopped.
    Not used by ImageAnalyzer.
    """

    ERROR = -1
    """An error occurred."""

    NO_MORE_DATA = 0
    """The end of the input stream was reached."""

    STOP_REQUESTED = 1
    """An API call was made to stop analysis."""


class SessionStoppedErrorReason(Enum):
    """
    Defines reasons why the session stopped erroneously.
    Not used by ImageAnalyzer.
    """

    AUTHENTICATION_FAILURE = 1
    """
    Indicates an authentication error.
    An authentication error occurs if subscription key or authorization token is invalid, expired,
    or does not match the region being used.
    """

    BAD_REQUEST = 2
    """Indicates that one or more recognition parameters are invalid or the audio format is not supported."""

    TOO_MANY_REQUESTS = 3
    """Indicates that the number of parallel requests exceeded the number of allowed concurrent transcriptions for the subscription."""

    FORBIDDEN = 4
    """Indicates that the free subscription used by the request ran out of quota."""

    CONNECTION_FAILURE = 5
    """Indicates a connection error."""

    SERVICE_TIMEOUT = 6
    """Indicates a time-out error when waiting for response from service."""

    SERVICE_ERROR = 7
    """Indicates that an error is returned by the service."""

    SERVICE_UNAVAILABLE = 8
    """Indicates that the service is currently unavailable."""

    RUNTIME_ERROR = 9
    """Indicates an unexpected runtime error."""


class SessionResultReason(Enum):
    """
    Defines reasons why the session stopped erroneously.
    Not used by ImageAnalyzer.
    """

    NO_MATCH = 0
    """
    Indicates the requested inference was not found. More details can be found using the NoMatchDetails.from_result method.
    """

    STOPPED = 1
    """Indicates the requested operation was stopped. More details can be found using the StoppedDetails.from_result method."""

    DETECTING = 2
    """Indicates preliminary or partial detection results are available."""

    DETECTED = 3
    """Indicates final and complete detection results are available."""

    RECOGNIZING = 4
    """Indicates preliminary or partial recognition results are available."""

    RECOGNIZED = 5
    """Indicates final and complete inference results are available."""
