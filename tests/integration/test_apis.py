from app.main import create_app
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def test_apis(integration_test_config):
    app = create_app(integration_test_config)
    client = app.test_client()

    # Test index endpoint
    payload = {
            "image_dir": integration_test_config.image_dir,
            "metadata_dir": integration_test_config.metadata_dir,
        }
    response = client.post(
        '/index',
        json=payload,
    )

    assert response.status_code == 200
    assert response.json['message'] == "Indexing completed"

    # Test search endpoint
    query_image_path = sorted(os.listdir(integration_test_config.image_dir))[2]
    query_image_path = os.path.join(integration_test_config.image_dir, query_image_path)

    with open(query_image_path, 'rb') as f:
        data = {
            'file': (f, os.path.basename(query_image_path), 'image/jpeg'),
        }

        response = client.post(
            '/upload',
            content_type='multipart/form-data',
            data=data,
        )

    assert response.status_code == 200
    response_json = response.get_json()
    assert 'search_id' in response_json
    assert 'processing_time_ms' in response_json
    logger.info(f"processing_time_ms: {response_json['processing_time_ms']}")
    assert 'retrieved_images' in response_json
    assert len(response_json['retrieved_images']) == integration_test_config.top_k
    assert response_json['retrieved_images'][0].split("/")[-1] == query_image_path.split("/")[-1]
    assert not os.listdir(integration_test_config.upload_dir)