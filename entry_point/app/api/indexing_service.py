from shared_contracts.protos.indexing_service.indexing_service_pb2_grpc import IndexingServiceStub
from shared_contracts.protos.indexing_service.indexing_service_pb2 import IndexImagesRequest, IndexImagesResponse
import grpc

from openapi_server.models.index_images_request import IndexImagesRequest as IndexImagesRequestRest
from openapi_server.models.index_images200_response import IndexImages200Response

import uuid


class IndexingService:
    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:50073")
        self.stub = IndexingServiceStub(self.channel)

    def index(self, index_request: IndexImagesRequestRest):
        job_id = str(uuid.uuid4())

        # Convert request protocol
        grpc_request = IndexImagesRequest(
            job_id=job_id,
            image_bucket=index_request.image_storage_bucket,
            metadata_bucket=index_request.metadata_storage_bucket,
        )
        
        # Call indexing service
        grpc_response: IndexImagesResponse = self.stub.index_images(grpc_request)

        # Convert response protocol
        return IndexImages200Response(
            job_id=grpc_response.job_id,
            message=grpc_response.message,
        )