import pytest
from qdrant_client import QdrantClient
from qdrant_client.models import Distance

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