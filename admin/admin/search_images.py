import requests

image_path = '/mnt/d/visual-search/tests/test_data/images/000001.jpg'
url = 'http://localhost/api/search'

with open(image_path, 'rb') as f:
    response = requests.post(
        url=url,
        files={'file': f},
    )