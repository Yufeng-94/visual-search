from pydantic import Field
from pydantic_settings import BaseSettings
import torch
from qdrant_client.models import Distance

class Settings(BaseSettings):

    device: torch.device = Field(
        default_factory=lambda: torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
            )
        )
    
    pre_trained_weights_cache_dir: str = "data/models"
    
    # Vector Db settings
    vector_db_name: str = "visual_search_db"
    vector_db_dimension: int = 2048
    vector_db_distance: Distance = Distance.COSINE
    # Change to Path
    vector_db_location: str = "data/vector_db"


    # Image storage settings
    image_storage_dir: str = "data/image_storage"
    
    # App settings
    upload_dir: str = "upload"
    max_content_length: int = 16 * 1024 *1024

    # Search service settings
    top_k: int = 4

    # Indexing service settings
    batch_size: int = 32
    parallel: int = 4

    # Index page dir
    index_html_dir: str = 'index.html'


# TODO: convert to Path