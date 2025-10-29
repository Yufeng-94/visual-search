from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ImageRequest(_message.Message):
    __slots__ = ("query_image", "job_id")
    QUERY_IMAGE_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    query_image: bytes
    job_id: str
    def __init__(self, query_image: _Optional[bytes] = ..., job_id: _Optional[str] = ...) -> None: ...

class ImageResponse(_message.Message):
    __slots__ = ("encoded_image", "job_id")
    ENCODED_IMAGE_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    encoded_image: _containers.RepeatedScalarFieldContainer[float]
    job_id: str
    def __init__(self, encoded_image: _Optional[_Iterable[float]] = ..., job_id: _Optional[str] = ...) -> None: ...
