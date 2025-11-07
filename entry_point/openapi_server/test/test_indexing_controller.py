from openapi_server.__main__ import create_app
from openapi_server.models.index_images_request import IndexImagesRequest
from shared_contracts.protos.indexing_service.indexing_service_pb2 import IndexImagesResponse

from shared_contracts.protos.indexing_service.indexing_service_pb2_grpc import IndexingServiceServicer, add_IndexingServiceServicer_to_server

import json
import grpc
from concurrent import futures
import threading

class MockedIndexingServicer(IndexingServiceServicer):

    def index_images(self, request, context):

        return IndexImagesResponse(
            job_id="123e4567-e89b-12d3-a456-426614174000",
            success=True,
            message="Indexing successfully",
        )
def start_test_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    add_IndexingServiceServicer_to_server(MockedIndexingServicer(), server)
    server.add_insecure_port('[::]:50073')
    server.start()
    server.wait_for_termination()
    return server

def test_index_images():
    # Start a mocked indexing gRPC server
    thread = threading.Thread(target=start_test_server, daemon=True)
    thread.start()
    print("Test server started")

    # Note: Using the Flask test client directly, not via Connexion
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        print("Test client created")

        index_images_request = IndexImagesRequest(
            image_storage_bucket="test-bucket",
            metadata_storage_bucket="test-metadata-bucket"
        )
        print("Test request created")

        response = client.post(
            '/api/index',
            data=json.dumps(index_images_request.to_dict()) ,
            content_type='application/json'
        )
    
    thread.join(timeout=10)

    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['job_id'] == "123e4567-e89b-12d3-a456-426614174000"
    assert response_data['message'] == "Indexing successfully"