import boto3
from shared_contracts.storage.storage_contracts import StorageContracts
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams
from shared_contracts.vector_db.vector_db_contracts import VectorDBContracts

def remove_infra():
    qdrant_client = QdrantClient(
        host="localhost", 
        grpc_port=6334, 
        prefer_grpc=True,
        timeout=30,
    )

    s3_client = boto3.client(
        's3', 
        endpoint_url='http://localhost:4566',
        aws_access_key_id="test",  # Placeholder credentials
        aws_secret_access_key="test",  # Placeholder credentials
    )

    # remove existing collection for clean slate
    if qdrant_client.collection_exists(
        collection_name=VectorDBContracts.collection_name,
    ):
        qdrant_client.delete_collection(
            collection_name=VectorDBContracts.collection_name,
        )
        print(f"Deleted existing {VectorDBContracts.collection_name} collection in Qdrant")

    # Delete S3 buckets
    buckets_to_delete = [
        'source-image-bucket',
        'source-metadata-bucket',
        StorageContracts.indexing_dest_image_bucket,
    ]

    for bucket in buckets_to_delete:
        # Delete all objects in the bucket
        response = s3_client.list_objects_v2(Bucket=bucket)
        if 'Contents' in response:
            for obj in response['Contents']:
                s3_client.delete_object(Bucket=bucket, Key=obj['Key'])
                print(f"Deleted {obj['Key']} from {bucket}")
        # Delete the bucket itself
        s3_client.delete_bucket(Bucket=bucket)
        print(f"Deleted bucket {bucket}")

if __name__ == "__main__":
    remove_infra()