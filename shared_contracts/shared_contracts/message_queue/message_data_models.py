from pydantic import BaseModel
from typing import List

class ImageEncodingCommand(BaseModel):
    job_id: str
    image_url: str


class EncodingStart(BaseModel):
    job_id: str
    timestamp: str


class EncodingResults(BaseModel):
    job_id: str
    encoded_image: List[float]