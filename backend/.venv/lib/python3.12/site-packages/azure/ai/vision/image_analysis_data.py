# Copyright (c) Microsoft. All rights reserved.
# See https://aka.ms/azai/vision/license for the full license information.
"""
Classes that represents the data structures of vision image analysis results.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Rectangle:
    """
    Represents rectangular area inside an image.
    """
    x: int = 0
    """X-coordinate of the top left point of the area, in pixels."""

    y: int = 0
    """Y-coordinate of the top left point of the area, in pixels."""

    w: int = 0
    """Width of the area, in pixels."""

    h: int = 0
    """Height of the area, in pixels."""


@dataclass
class DetectedObject:
    """
    Represents a physical object detected in an image.
    """

    bounding_box: Rectangle
    """
    A rectangular boundary within which the object was detected.

    Coordinates are are in pixels, with (0,0) being the top-left of the source image.
    """

    name: str = ''
    """
    A label that briefly describes the detected object.
    """

    confidence: float = 0.0
    """
    A score that represents the likelihood that this detection was accurate.

    Confidence scores span the range of 0.0 to 1.0 (inclusive), with higher values indicating higher probability.
    """


@dataclass
class DetectedObjects(List[DetectedObject]):
    """
    Represents a list of physical object detected in an image.
    """
    pass


@dataclass
class ContentTag:
    """
    Represent an image tag. A tag can be a recognizable object, living being, scenery, or actions that appear in the image.
    """

    name: str = ''
    """
    The name of the tag.

    Note that you can control the tag language by calling ImageAnalysisOptions.language.
    """

    confidence: float = 0.0
    """
    A score that represents the likelihood that this detection was accurate.

    Confidence scores span the range of 0.0 to 1.0 (inclusive), with higher values indicating higher probability.
    """


@dataclass
class ContentTags(List[ContentTag]):
    """
    Represents a list of image tags

    """
    pass


@dataclass
class DetectedPerson:
    """
    Represents a person detected in an image.
    """

    bounding_box: Rectangle
    """
    A rectangular boundary within which the person was detected.

    Coordinates are are in pixels, with (0,0) being the top-left of the source image.
    """

    confidence: float = 0.0
    """
    A score that represents the likelihood that this detection was accurate.

    Confidence scores span the range of 0.0 to 1.0 (inclusive), with higher values indicating higher probability.
    """


@dataclass
class DetectedPeople(List[DetectedPerson]):
    """
    Represents people detected in the image.
    """
    pass


@dataclass
class CropSuggestion:
    """
    Represents a suggested image cropping that preserves much of the image content.
    """

    bounding_box: Rectangle
    """
    A rectangular boundary of the crop suggestion.

    Coordinates are are in pixels, with (0,0) being the top-left of the source image.
    """

    aspect_ratio: float = 0.0
    """
    The aspect ratio of this crop suggestion.

    Aspect ratios are calculated by dividing the width of the cropped region by its height.

    You can request particular aspect ratios by calling setting ImageAnalysisOptions.cropping_aspect_ratios.

    aspect_ratio will be in the range 0.75 to 1.8 (inclusive) if ImageAnalysisOptions.cropping_aspect_ratios
    was called, otherwise it will be in the range 0.5 to 2.0 (inclusive).
    """


@dataclass
class CropSuggestions(List[CropSuggestion]):
    """
     Represents a list of image crop suggestions that preserve most of the image content.
    """
    pass


@dataclass
class ContentCaption:
    """
    Represents a generated phrase that describes the content of the image.
    """

    bounding_box: Rectangle
    """
    A rectangular boundary to which the caption applies.

    Coordinates are are in pixels, with (0,0) being the top-left of the source image.
    For the ImageAnalysisFeature.CAPTION result, this will be the whole image.
    For the ImageAnalysisFeature.DENSE_CAPTIONS results, this will either be the whole image
    or a region within the image.
    """

    content: str = ''
    """
    A generated phrase that describes the content of the image.
    """

    confidence: float = 0.0
    """
    A score, in the range of 0 to 1, representing the confidence that this caption is accurate.

    Confidence scores span the range of 0.0 to 1.0 (inclusive), with higher values indicating higher probability.
    """


@dataclass
class DenseCaptions(List[ContentCaption]):
    """
    Represents a list of up to 10 captions for different regions of the image.
    The first caption in the list represents the the whole image, and it is identical to the result
    returned if you select the option ImageAnalysisFeature.CAPTION.
    """
    pass


@dataclass
class DetectedTextWord:
    """
    Represents a single word that was detected in an image.

    Words consist of a contiguous sequence of characters.
    For non-space delimited languages such as Chinese, Japanese, and Korean, each character is represented as its own word.

    """

    content: str
    """
    The text detected within the bounds of this word.
    """

    bounding_polygon: List[int]
    """
    A bounding polygon with points that enclose the word.

    These points are polygon vertices, presented in clockwise order from the left (-180 degrees, inclusive)
    relative to the region's orientation. Coordinates are are in pixels, with (0,0) being the top-left of the source image.
    """

    confidence: float = 0.0
    """
    A score that represents the likelihood that this detection was accurate.

    Confidence scores span the range of 0.0 to 1.0 (inclusive), with higher values indicating higher probability.
    """


@dataclass
class DetectedTextLine:
    """
    Represents a single, contiguous line of text as detected within an image.
    """

    content: str
    """
    The text detected in this line.
    """

    bounding_polygon: List[int]
    """
    A bounding polygon with points that enclose this line of text.

    These points are polygon vertices, presented in clockwise order from the left (-180 degrees, inclusive)
    relative to the region's orientation. Coordinates are are in pixels, with (0,0) being the top-left of the source image.
    """

    words: List[DetectedTextWord]
    """
    A list of detected words associated with this line.
    """


@dataclass
class DetectedText:
    """
    Represents the text lines detected in an image.
    """

    lines: List[DetectedTextLine]
    """
    The full list of all lines of text detected in an image.
    """


@dataclass
class SegmentationResult:
    """
    Holds a single segmentation result image of PNG format and associated metadata.
    """

    image_height: int = 0
    """
    The image height in pixels.
    """

    image_width: int = 0
    """
    The image width in pixels.
    """

    image_buffer: bytes = ''
    """
    The result image buffer in PNG format.
    """
