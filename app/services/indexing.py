import json
from typing import List
from app.db.vector_db import VectorDB
from app.db.image_storage import ImageStorage
from app.models.image_encoder import PreTrainedImageEncoder
import torch
import torchvision
import logging
from torchvision.io import decode_image

METADATA_ITEM_KEYS = ['scale', 'viewpoint', 'zoom_in', 'style', 'bounding_box', 'occlusion', 'category_id']

class IndexService:
    """
    <Description>

    """
    def __init__(
            self, 
            vector_db: VectorDB,
            image_storage: ImageStorage,
            image_encoder: PreTrainedImageEncoder,
            image_process: torchvision.transforms, # TBD: type
            device: torch.device,
            ):
        self.vector_db = vector_db
        self.image_encoder = image_encoder
        self.image_process = image_process
        self.image_storage = image_storage
        self.device = device

    def index_images(
            self,
            image_paths: list[str], 
            metadata_paths: list[str],
            batch_size: int,
            parallel: int,
            ):

        # Index images by batch
        for i in range(0, len(image_paths), batch_size):
            try:
                # prepare batch
                batch_image_paths = image_paths[i: i+batch_size]
                batch_metadata_paths = metadata_paths[i: i+batch_size]
            except Exception as e:
                logging.error(f"Failed to prepare batch {i//batch_size}.")
                raise e

            try:
                # Upload images to image storage
                image_urls = self.image_storage.upload_images(batch_image_paths)
            except Exception as e:
                logging.error(f"Failed to upload images to image storage: {e}")
                raise e

            try:
                # get image metadata
                batch_metedata = self._load_metadata(batch_metadata_paths, batch_image_paths)
                # add image URLs to metadata
                for j in range(len(batch_metedata)):
                    batch_metedata[j]['image_url'] = image_urls[j]
            except Exception as e:
                logging.error(f"Failed to load metadata for batch {i//batch_size}: {e}")
                raise e

            try:
                # get image tensors
                batch_image_tensors = self._load_process_images(batch_image_paths, self.image_process)
                batch_image_tensors = batch_image_tensors.to(self.device)

                # batch encode images
                with torch.no_grad():
                    batch_image_embeddings = self.image_encoder(batch_image_tensors)
                batch_image_embeddings = batch_image_embeddings.cpu().numpy().tolist()

                # Upload to vector DB
                self.vector_db.add_batch_images(
                    image_embeddings=batch_image_embeddings, 
                    metadata_list=batch_metedata,
                    parallel=parallel,
                )
                
                logging.info(f"Added {len(batch_image_paths)} images to Qdrant collection '{self.vector_db.database_name}'.")

            except Exception as e:
                logging.error(f"Failed to add images to Qdrant collection '{self.vector_db.database_name}': {e}")
                raise e


    def _load_process_images(
            self, 
            image_paths: List[str], 
            transforms: torchvision.transforms.Compose,
            ) -> torch.Tensor:
        
        image_tensors = []
        for p in image_paths:
            image_tensor = decode_image(p) # [3, H, W]
            image_tensor = transforms(image_tensor) # [3, H, W]
            image_tensors.append(image_tensor)

        return torch.stack(image_tensors, dim=0) # [batch_size, 3, H, W]

    def _load_metadata(
            self, 
            metadata_paths: List[str], 
            image_paths: List[str]
            ) -> List[dict]:
        
        loaded_metadata = []
        for m_p, i_p in zip(metadata_paths, image_paths):
            # Load metadata JSON
            with open(m_p, 'r') as f:
                metadata_raw = json.load(f)

            # Prepare extracted metadata
            metadata = {}
            metadata['segmented'] = False
            for k, v in metadata_raw.items():
                if 'item' in k:
                    item_metadata = {}
                    for i_k in METADATA_ITEM_KEYS:
                        item_metadata[i_k] = v.get(i_k, None)
                    metadata[k] = item_metadata
                else:
                    metadata[k] = v

            # Add other metadata
            ## NOTE: could replace with Path
            metadata['image_name'] = m_p.split('/')[-1].replace('.json', '')

            loaded_metadata.append(metadata)

        return loaded_metadata
