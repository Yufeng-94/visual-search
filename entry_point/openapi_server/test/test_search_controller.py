from openapi_server.__main__ import create_app
from shared_contracts.protos.search_service.search_service_pb2 import SearchResponse, ImageResult

from shared_contracts.protos.search_service.search_service_pb2_grpc import SearchServiceServicer, add_SearchServiceServicer_to_server

import grpc
from concurrent import futures
import threading
import pytest

class MockedSearchServicer(SearchServiceServicer):

    def search(self, request, context):

        return SearchResponse(results=[
            ImageResult(
                image_url="http://example.com/image1.jpg",
                similarity_score=0.95
            ),
            ImageResult(
                image_url="http://example.com/image2.jpg",
                similarity_score=0.90
            )
        ])
    
def start_test_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    add_SearchServiceServicer_to_server(MockedSearchServicer(), server)
    server.add_insecure_port('[::]:50071')
    server.start()
    server.wait_for_termination()
    return server

def test_search():
    # Start a mocked indexing gRPC server
    thread = threading.Thread(target=start_test_server, daemon=True)
    thread.start()
    print("Test server started")

    # Note: Using the Flask test client directly, not via Connexion
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        print("Test client created")

        image_file = "openapi_server/test/test_image.jpg"
        with open(image_file, 'rb') as f:
            data = {'file': f}
            print("Test image loaded")

            response = client.post(
                '/api/search',
                data=data,
                content_type='multipart/form-data'
            )
    
    thread.join(timeout=10)

    assert response.status_code == 200
    response_data = response.get_json()
    similar_images = response_data['similar_images']
    assert similar_images[0]['image_url'] == "http://example.com/image1.jpg"
    assert similar_images[0]['similarity_score'] == pytest.approx(0.95)
    assert similar_images[1]['image_url'] == "http://example.com/image2.jpg"
    assert similar_images[1]['similarity_score'] == pytest.approx(0.90)