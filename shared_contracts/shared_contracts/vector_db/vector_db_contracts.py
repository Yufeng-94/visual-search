from qdrant_client.models import Distance

class VectorDBContracts:
    collection_name: str = "visual_search_db"
    dimension: int = 2048
    distance_metric: Distance = Distance.COSINE 