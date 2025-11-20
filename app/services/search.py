from typing import List
import torch
import torchvision
from torchvision.io import decode_image
from qdrant_client.models import ScoredPoint
import logging
from app.db.vector_db import VectorDB
from app.db.image_storage import ImageStorage
from app.models.image_encoder import PreTrainedImageEncoder


class SearchService:
    """
    <Description>
    """
    def __init__(
            self, 
            vector_db: VectorDB,
            image_storage: ImageStorage,
            image_encoder: PreTrainedImageEncoder,
            image_process: torchvision.transforms.Compose,
            device: torch.device,
            ):
        self.vector_db = vector_db
        self.image_encoder = image_encoder
        self.image_process = image_process
        self.image_storage = image_storage
        self.device = device

    def search(self, 
               input_image_path: str,
               top_k: int,
               ) -> List[str]:

        # Load input image
        input_image = decode_image(input_image_path) # (3, H, W)
        logging.info(f"image decoded, image size: {input_image.size()}")

        # Process input image
        image_processed = self.image_process(input_image).unsqueeze(0).to(self.device) # (1, 3, H, W)
        logging.info(f"image processed, image size: {image_processed.size()}")

        # Get image embedding
        try:
            with torch.no_grad():
                image_embedding = self.image_encoder(image_processed)
            image_embedding = image_embedding.squeeze(0).cpu().numpy() # (2048, )

            logging.info(f"image encoded, embedding size: {image_embedding.shape}")
        except Exception as e:
            logging.error(f"Failed to get image embedding: {e}")

        # Search in vector DB
        results = self.vector_db.query_image(image_embedding, top_k)
        logging.info(f"image searched, found {len(results)} results")

        image_urls = self._extract_urls_from_results(results)
        logging.info(f"image URLs extracted, found {len(image_urls)} URLs")

        # Query image storage to get valid image URLs
        retrieved_images_urls = self.image_storage.query_images(image_urls)
        logging.info(f"image URLs queried from storage, found {len(retrieved_images_urls)} valid URLs") 

        return retrieved_images_urls

    def _extract_urls_from_results(self, results: List[ScoredPoint]) -> List[str]:
        image_urls = [point.payload.get('image_url', None) for point in results]

        return image_urls



