from typing import List
import torch
import torchvision
from qdrant_client.models import ScoredPoint

from app.db.vector_db import VectorDB
from app.db.image_storage import ImageStorage  # TBD: type
from app.models.image_encoder import PreTrainedImageEncoder


class SearchService:
    """
    <Description>
    """
    def __init__(
            self, 
            vector_db: VectorDB,
            image_storeage, # TBD: type
            image_encoder: PreTrainedImageEncoder,
            image_process: torchvision.transforms, # TBD: type
            device: torch.device,
            ):
        self.vector_db = vector_db
        self.image_encoder = image_encoder
        self.image_process = image_process
        self.image_storage = image_storeage
        self.device = device

    def search(self, 
               input_image, # type TBD
               top_k: int,
               ) -> torch.Tensor: # return type TBD


        # Process input image
        image_processed = self.image_process(input_image).unsqueeze(0).to(self.device) # (1, 3, H, W)

        # Get image embedding
        image_embedding = self.image_encoder(image_processed)
        image_processed = image_processed.squeeze(0).cpu().numpy() # (3, H, W)

        # Search in vector DB
        results = self.vector_db.query_image(image_embedding, top_k)
        image_urls = extract_urls_from_results(results)

        # Load retrieved image from image storage
        retrieved_images = self.image_storage.query_images(image_urls)
        retrieved_images = convert_to_tensor(retrieved_images)

        return retrieved_images

def extract_urls_from_results(results: List[ScoredPoint]) -> List[str]:
    pass

def convert_to_tensor(images: List) -> torch.Tensor:
    pass


