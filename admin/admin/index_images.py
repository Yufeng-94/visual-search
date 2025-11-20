import requests
import json
# Directly send request to indexing service
request_data = {
    'image_storage_bucket': 'source-image-bucket',
    'metadata_storage_bucket': 'source-metadata-bucket',
}

url = 'http://localhost:8000/api/index'

response = requests.post(
    url=url,
    json=request_data,
)