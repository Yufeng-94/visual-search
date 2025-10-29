from proto.image_encoding_service_pb2_grpc import ImageEncodingServiceServicer
from proto.image_encoding_service_pb2 import ImageRequest, ImageResponse

from grpc import ServicerContext
from torchvision.io import decode_image
import torch
import os

from app.image_encoder_loader import load_image_encoder

class ImageEncodingServicer(ImageEncodingServiceServicer):
    def __init__(
            self, 
            device: torch.device = torch.device('cpu'),
        ):

        self.device = device

        self.image_encoder, self.image_process = load_image_encoder(
            device=self.device
        )

    def encode_image(
            self, 
            request: ImageRequest, 
            context: ServicerContext,
        ):

        job_id = request.job_id
        
        image_bytes = request.query_image
        input_tensor = torch.frombuffer(
            image_bytes, dtype=torch.uint8
        ).clone() # Copy to a writable tensor
        image_tensor = decode_image(input_tensor) # (C, H, W)

        image_processed = self.image_process(image_tensor).unsqueeze(0).to(self.device) # (1, C, H, W)
        with torch.no_grad():
            image_embedding = self.image_encoder(image_processed)
        image_embedding = image_embedding.squeeze(0).cpu().numpy() # (D,)

        return ImageResponse(
            job_id=job_id,
            encoded_image=image_embedding,
        )
        
