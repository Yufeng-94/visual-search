import boto3
from shared_contracts.storage.storage_contracts import StorageContracts
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams
from shared_contracts.vector_db.vector_db_contracts import VectorDBContracts

def create_infra():
    # Create infra
    s3_client = boto3.client(
        's3', 
        endpoint_url='http://localhost:4566',
        aws_access_key_id="test",  # Placeholder credentials
        aws_secret_access_key="test",  # Placeholder credentials
    )
    qdrant_client = QdrantClient(
        host="localhost", 
        grpc_port=6334, 
        prefer_grpc=True,
        timeout=30,
    )
    
    # Create S3 buckets
    s3_client.create_bucket(Bucket='source-image-bucket')
    print("Created source-image-bucket")
    s3_client.create_bucket(Bucket='source-metadata-bucket')
    print("Created source-metadata-bucket")
    s3_client.create_bucket(Bucket=StorageContracts.indexing_dest_image_bucket)
    print(f"Created {StorageContracts.indexing_dest_image_bucket}")
    # Create Vector DB collections
    if not qdrant_client.collection_exists(
    collection_name=VectorDBContracts.collection_name,
):
        qdrant_client.create_collection(
            collection_name=VectorDBContracts.collection_name,
            vectors_config=VectorParams(
                    size=VectorDBContracts.dimension,
                    distance=VectorDBContracts.distance_metric,
                )
        )
        print(f"Created {VectorDBContracts.collection_name} collection in Qdrant")
    else:
        print(f"{VectorDBContracts.collection_name} collection already exists in Qdrant")
    
    #  Upload test image and metadata to source buckets
    for i in range(30, 51):
        image_name = f'0000{i}.jpg'
        metadata_name = f'0000{i}.json'
        image_path = f'data/images/{image_name}'
        metadata_path = f'data/metadata/{metadata_name}'

        with open(image_path, 'rb') as img_file:
            s3_client.upload_fileobj(
                img_file,
                'source-image-bucket',
                image_name,
            )
        print(f"Uploaded {image_name} to source-image-bucket")

        with open(metadata_path, 'rb') as metadata_file:
            s3_client.upload_fileobj(
                metadata_file,
                'source-metadata-bucket',
                metadata_name,
            )
        print(f"Uploaded {metadata_name} to source-metadata-bucket")

if __name__ == "__main__":
    create_infra()