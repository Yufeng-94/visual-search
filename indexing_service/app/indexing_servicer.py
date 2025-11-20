from shared_contracts.protos.indexing_service.indexing_service_pb2_grpc import (
    IndexingServiceServicer,
)
from shared_contracts.protos.indexing_service.indexing_service_pb2 import (
    IndexImagesResponse,
    IndexImagesRequest,
)
from shared_contracts.storage.storage_contracts import StorageContracts
from shared_contracts.message_queue.message_channels import MessageChannels
import asyncio
from grpc import ServicerContext
import boto3
from qdrant_client import QdrantClient
import redis
from app.image_indexing import (
    get_image_keys_from_s3,
    create_metadata_keys_from_image_keys,
    process_single_image,
)

from app.message_routing import (
    start_redis_router,
)

import logging

logger = logging.getLogger("indexing_service.indexing_servicer")

class IndexingServicer(IndexingServiceServicer):
    def __init__(self):
        self.s3_client = boto3.client(
                's3', 
                endpoint_url='http://localstack:4566',
                aws_access_key_id="test",  # Placeholder credentials
                aws_secret_access_key="test",  # Placeholder credentials
                )
        
        self.qdrant_client = QdrantClient(
            host="qdrant", 
            grpc_port=6334, 
            prefer_grpc=True,
            timeout=30,
        )

        self.redis_client = redis.Redis(
            host='redis', 
            port=6379, 
        )

        self.router_started = False


    def index_images(
            self, 
            request: IndexImagesRequest, 
            context: ServicerContext
        ) -> IndexImagesResponse:
        
        indexing_job_id = request.job_id
        src_image_bucket = request.image_bucket
        metadata_bucket = request.metadata_bucket
        dest_image_bucket = StorageContracts.indexing_dest_image_bucket

        # get image keys from external storage
        image_keys = get_image_keys_from_s3(
            self.s3_client, 
            src_image_bucket,
        )
        metadata_keys = create_metadata_keys_from_image_keys(image_keys)

        if not self.router_started:
            start_redis_router(
                MessageChannels.INDEXING_EVENTS,
                self.redis_client,
            )
            self.router_started = True
            logger.info(f"Started Redis router for {MessageChannels.INDEXING_EVENTS}")
        try:
            responses = [
                process_single_image(
                    src_image_bucket,
                    image_key,
                    metadata_bucket,
                    metadata_key,
                    dest_image_bucket,
                    self.s3_client,
                    self.qdrant_client,
                    self.redis_client,
                )
                for image_key, metadata_key in zip(image_keys, metadata_keys)
            ]
        except Exception as e:
            logger.error(f"Indexing failed due to error: {e}")
            raise Exception(f"Indexing failed due to error {e}")

        return IndexImagesResponse(
            job_id=indexing_job_id,
            success=True,
            message=str(responses)
        )

