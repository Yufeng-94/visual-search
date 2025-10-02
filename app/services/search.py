from typing import List
import torch
import torchvision
from torchvision.io import decode_image
from qdrant_client.models import ScoredPoint

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

        # Process input image
        image_processed = self.image_process(input_image).unsqueeze(0).to(self.device) # (1, 3, H, W)

        # Get image embedding
        with torch.no_grad():
            image_embedding = self.image_encoder(image_processed)
            image_embedding = image_embedding.squeeze(0).cpu().numpy() # (2048, )

        # Search in vector DB
        results = self.vector_db.query_image(image_embedding, top_k)
        image_urls = self._extract_urls_from_results(results)

        # Query image storage to get valid image URLs
        retrieved_images_urls = self.image_storage.query_images(image_urls)

        return retrieved_images_urls

    def _extract_urls_from_results(self, results: List[ScoredPoint]) -> List[str]:
        image_urls = [point.payload.get('image_url', None) for point in results]

        return image_urls



