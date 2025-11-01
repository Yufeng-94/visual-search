import uuid
import redis
import asyncio
import boto3
import json
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from shared_contracts.message_queue.message_data_models import ImageEncodingCommand, EncodingResults
from shared_contracts.message_queue.message_contract import MessageContract
from shared_contracts.vector_db.vector_db_contracts import VectorDBContracts
from app.message_routing import result_queue, add_to_result_queue
from app.process_image_metadata import extract_useful_metadata

import time

def process_single_image(
        src_image_bucket: str, 
        image_key: str,
        metadata_bucket: str,
        metadata_key: str,
        dest_image_bucket: str,
        s3_client,
        qdrant_client,
        redis_client: redis.Redis,
        ):
    try:
        job_id = str(uuid.uuid4())
        print(f"Processing image {image_key} with job_id {job_id}")

        # Send url to message queue
        send_image_encoding_command(
            src_image_bucket,
            image_key,
            job_id, 
            redis_client
            )
        print(f"Sent encoding command for {image_key} with job_id {job_id}")

        # Wait for processing result
        encoding_result = wait_for_model_result_sync(job_id, timeout=60)
        print(f"Received encoding result for {image_key} with job_id {job_id}")

        # Save image to S3
        save_image_to_s3(
            s3_client, src_image_bucket, dest_image_bucket, image_key
            )
        print(f"Saved image {image_key} to destination bucket {dest_image_bucket}")

        # Add S3 url to metadata
        image_metadata = process_metadata(
            metadata_bucket, 
            metadata_key, 
            dest_image_bucket, 
            image_key,
            s3_client,
            )
        print(f"Processed metadata for image {image_key}")

        # Store metadata and image embedding in vector DB
        store_in_vector_db(
            qdrant_client, 
            image_metadata, 
            encoding_result,        
        )
        print(f"Stored image embedding and metadata for {image_key} in vector DB")

        # Return processing status
        return "PROCESSED"
    
    except Exception as e:
        return f"FAILED: {str(e)}"

def send_image_encoding_command(
        external_image_bucket: str, 
        image_key: str, 
        job_id: str, 
        redis_client: redis.Redis
        ) -> str:
    image_encoding_command = ImageEncodingCommand(
        job_id=job_id,
        image_bucket=external_image_bucket,
        image_key=image_key,
    )

    image_encoding_msg_channel = MessageContract.get_channel_for_message(type(image_encoding_command))

    _ = redis_client.xadd(
        image_encoding_msg_channel, 
        {'data': image_encoding_command.model_dump_json()},
        )
    
    queue = add_to_result_queue(job_id)

    return queue

def wait_for_model_result_sync(
        job_id: str, timeout: int = 60
        ) -> EncodingResults:
    
    queue = result_queue[job_id]

    try:
        encoding_results = queue.get(timeout=timeout)
        return encoding_results

    except Exception as e:
        raise Exception(f"Error waiting for model result for job_id: {job_id}, error: {str(e)}")

    finally:
        if job_id in result_queue:
            del result_queue[job_id]

def save_image_to_s3(
        s3_client: boto3.client, 
        src_image_bucket: str, 
        dest_image_bucket: str,
        image_key: str
        ) -> None:
    try:
        copy_source = {
            'Bucket': src_image_bucket,
            'Key': image_key
        }

        s3_client.copy(
            CopySource=copy_source,
            Bucket=dest_image_bucket,
            Key=image_key
        )
    except Exception as e:
        raise Exception(f"Error saving image to S3: {str(e)}")

def process_metadata(
        metadata_bucket: str, 
        metadata_key: str, 
        image_bucket: str, 
        image_key: str,
        s3_client: boto3.client
        ) -> dict:
    
    # Download metadata
    print(f"Downloading metadata {metadata_key} from {metadata_bucket}")
    response = s3_client.get_object(
        Bucket=metadata_bucket,
        Key=metadata_key
    )
    metadata_content = response['Body'].read().decode('utf-8')
    metadata = json.loads(metadata_content)

    # Extract useful metadata
    metadata = extract_useful_metadata(metadata)

    # Add S3 image URL to metadata
    metadata["image_bucket"] = image_bucket
    metadata["image_key"] = image_key

    return metadata

def store_in_vector_db(
        qdrant_client: QdrantClient, 
        image_metadata: dict, 
        encoding_result: EncodingResults,
        collection_name: str = VectorDBContracts.collection_name,
        ):

    try:   
        point = PointStruct(
            id=encoding_result.job_id,
            vector=encoding_result.encoded_image,
            payload=image_metadata,
        )
        qdrant_client.upsert(
            collection_name=collection_name,
            points=[point],
        )
    except Exception as e:
        raise Exception(f"Error storing data in vector DB: {str(e)}")

def get_image_keys_from_s3(
        s3_client: boto3.client, 
        src_image_bucket: str, 
        ) -> List[str]:
    
    paginator = s3_client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=src_image_bucket)
    image_keys = []
    for page in page_iterator:
        if 'Contents' in page:
            for obj in page['Contents']:
                image_keys.append(obj['Key'])

    return image_keys

def create_metadata_keys_from_image_keys(image_keys: List[str]) -> List[str]:
    metadata_keys = []
    for image_key in image_keys:
        base_name = image_key.rsplit('.', 1)[0]
        metadata_key = f"{base_name}.json"
        metadata_keys.append(metadata_key)
    return metadata_keys


    