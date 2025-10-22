from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SearchRequest(_message.Message):
    __slots__ = ("jpg_image", "max_results")
    JPG_IMAGE_FIELD_NUMBER: _ClassVar[int]
    MAX_RESULTS_FIELD_NUMBER: _ClassVar[int]
    jpg_image: bytes
    max_results: int
    def __init__(self, jpg_image: _Optional[bytes] = ..., max_results: _Optional[int] = ...) -> None: ...

class SearchResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[ImageResult]
    def __init__(self, results: _Optional[_Iterable[_Union[ImageResult, _Mapping]]] = ...) -> None: ...

class ImageResult(_message.Message):
    __slots__ = ("image_url", "similarity_score", "width", "height")
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    SIMILARITY_SCORE_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    image_url: str
    similarity_score: float
    width: int
    height: int
    def __init__(self, image_url: _Optional[str] = ..., similarity_score: _Optional[float] = ..., width: _Optional[int] = ..., height: _Optional[int] = ...) -> None: ...
