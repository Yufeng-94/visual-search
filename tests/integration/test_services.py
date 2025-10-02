import os
import logging
from app.models.model_loader import load_image_encoder
from app.db.vector_db_loader import load_vector_db
from app.db.image_storage import ImageStorage
from app.services.search import SearchService
from app.services.indexing import IndexService

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def test_index_and_search_services(integration_test_config):
    os.environ['TORCH_HOME'] = integration_test_config.pre_trained_weights_cache_dir
    if not os.path.exists(integration_test_config.pre_trained_weights_cache_dir):
        os.makedirs(integration_test_config.pre_trained_weights_cache_dir)

    # Init model, db, storage
    logger.info("Loading model, vector db, and image storage...")
    image_encoder, image_process = load_image_encoder(
        integration_test_config.device
    )

    vector_db = load_vector_db(
        database_name=integration_test_config.vector_db_name,
        dimension=integration_test_config.vector_db_dimension,
        distance=integration_test_config.vector_db_distance,
        location=integration_test_config.vector_db_location,
    )

    image_storage = ImageStorage(
        image_dir=integration_test_config.image_storage_dir,
    )
    # Init services
    logger.info("Initializing indexing and search services...")
    search_service = SearchService(
        vector_db=vector_db,
        image_storage=image_storage,
        image_encoder=image_encoder,
        image_process=image_process,
        device=integration_test_config.device,
    )

    index_service = IndexService(
        vector_db=vector_db,
        image_storage=image_storage,
        image_encoder=image_encoder,
        image_process=image_process,
        device=integration_test_config.device,
    )

    # Test indexing
    logger.info("Testing indexing service...")
    image_dir = integration_test_config.image_dir
    metadata_dir = integration_test_config.metadata_dir

    image_path = sorted(os.listdir(image_dir))
    image_path = [os.path.join(image_dir, p) for p in image_path]
    metadata_path = sorted(os.listdir(metadata_dir))
    metadata_path = [os.path.join(metadata_dir, p) for p in metadata_path]
    
    index_service.index_images(
        image_paths=image_path,
        metadata_paths=metadata_path,
        batch_size=integration_test_config.batch_size,
        parallel=integration_test_config.parallel,
    )

    assert vector_db.get_number_of_vectors() == len(image_path)
    assert len(os.listdir(integration_test_config.image_storage_dir)) == len(image_path)
    assert vector_db.database_name == integration_test_config.vector_db_name
    
    # Test searching
    logger.info("Testing search service...")
    query_image_path = sorted(os.listdir(image_dir))[2]
    query_image_path = os.path.join(image_dir, query_image_path)
    search_results = search_service.search(
        input_image_path=query_image_path,
        top_k=integration_test_config.top_k,
    )
    assert len(search_results) == integration_test_config.top_k
    # assert the most similar image is the query image itself
    assert search_results[0].split("/")[-1] == query_image_path.split("/")[-1]

    logger.info("Integration test for indexing and searching workflow passed.")

    # Clean up
    vector_db.remove_db(
        integration_test_config.vector_db_name, 
        integration_test_config.vector_db_location, 
        vector_db.client
        )
    image_storage.clear_storage()
    
