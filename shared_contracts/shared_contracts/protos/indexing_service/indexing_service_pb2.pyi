from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class IndexImagesRequest(_message.Message):
    __slots__ = ("job_id", "image_bucket_url")
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    IMAGE_BUCKET_URL_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    image_bucket_url: str
    def __init__(self, job_id: _Optional[str] = ..., image_bucket_url: _Optional[str] = ...) -> None: ...

class IndexImagesResponse(_message.Message):
    __slots__ = ("job_id", "success", "message")
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    success: bool
    message: str
    def __init__(self, job_id: _Optional[str] = ..., success: bool = ..., message: _Optional[str] = ...) -> None: ...
