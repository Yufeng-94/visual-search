import argparse
import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Fetch image dir and metadata dir into request
parser = argparse.ArgumentParser()
parser.add_argument('--image-dir', required=True, help='Path to image directory')
parser.add_argument('--metadata-dir', required=True, help='Path to metadata directory')
parser.add_argument('--server-url', required=True, help='Server URL endpoint')

args = parser.parse_args()
image_dir = args.image_dir
metadata_dir = args.metadata_dir
server_url = args.server_url

# Send request to server URL
data = {
    'image_dir': image_dir, 
    'metadata_dir': metadata_dir,
}

response = requests.post(
    url=server_url,
    json=data,
    headers={'Content-Type': 'application/json'},
)

if response.status_code == 200:
    result = response.json()
    logger.info(f"Success: {result}")

else:
    logger.error(f"Error: {response.status_code, response.text}")

