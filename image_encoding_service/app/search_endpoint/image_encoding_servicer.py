from shared_contracts.protos.image_encoding_service.image_encoding_service_pb2_grpc import ImageEncodingServiceServicer
from shared_contracts.protos.image_encoding_service.image_encoding_service_pb2 import ImageRequest, ImageResponse

from grpc import ServicerContext
from torchvision.io import decode_image
import torch
import numpy as np

from app.image_encoder.image_encoder_loader import load_image_encoder

import logging

logger = logging.getLogger("image_encoding_service.servicer") # Inherits module logger

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
        ) -> ImageResponse:

        job_id = request.job_id
        
        logger.info("Parsing image...")
        image_bytes = request.query_image
        buf = np.frombuffer(image_bytes, dtype=np.uint8).copy()
        image_tensor = torch.from_numpy(buf)
        image_tensor = decode_image(image_tensor) # (C, H, W)

        image_processed = self.image_process(image_tensor).unsqueeze(0).to(self.device) # (1, C, H, W)
        logger.info("Encoding image...")
        with torch.no_grad():
            image_embedding = self.image_encoder(image_processed)
        image_embedding = image_embedding.squeeze(0).cpu().numpy() # (D,)
        image_embedding = image_embedding.tolist()
        logger.info(f"Embedded image size: {len(image_embedding)}")

        return ImageResponse(
            job_id=job_id,
            encoded_image=image_embedding,
        )
        
