import pytest
from qdrant_client import QdrantClient
from qdrant_client.models import Distance

from pydantic import Field
from pydantic_settings import BaseSettings
import torch

# TODO: convert to Path

@pytest.fixture
def vector_db_config() -> dict:
    return {
        "database_name": "test_db",
        "location": "tests/integration/vector_db_test",
        "distance": Distance.COSINE,
        "dimension": 10,
    }

@pytest.fixture
def qdrant_client(vector_db_config) -> QdrantClient:
    location = vector_db_config['location']

    return QdrantClient(path=location)


class IntegrationTestSettings(BaseSettings):

    supported_image_format: list[str] = ['.jpg', 'jpeg']

    device: torch.device = Field(
        default_factory=lambda: torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
            )
        )
    
    max_content_length: int = 16 * 1024 * 1024  # 16 MB
    
    pre_trained_weights_cache_dir: str = "tests/integration/data/models"
    
    # Vector Db settings
    vector_db_name: str = "integration_test_db"
    vector_db_dimension: int = 2048
    vector_db_distance: Distance = Distance.COSINE
    # Change to Path
    vector_db_location: str = "tests/integration/data/vector_db_test"

    # File upload settings
    upload_dir: str = "tests/integration/data/uploaded_images"


    # Image storage settings
    image_storage_dir: str = "tests/integration/data/image_storage_test"

    # Search service settings
    top_k: int = 3

    # Indexing service settings
    batch_size: int = 8
    parallel: int = 1

    image_dir: str = "tests/test_data/images"
    metadata_dir: str = "tests/test_data/metadata"

test_settings = IntegrationTestSettings()

@pytest.fixture
def integration_test_config():
    return test_settings
