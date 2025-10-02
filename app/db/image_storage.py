from typing import List
import os
import shutil

class ImageStorage:
    """
    <Description>
    """
    def __init__(self, image_dir: str):

        self.image_dir = image_dir

        # Create image directory if not exists
        if not os.path.exists(self.image_dir):
            os.mkdir(self.image_dir)

    def upload_images(self, image_paths: List[str]) -> List[str]:
        # save images to storage
        returned_image_urls = []
        for p in image_paths:
            image_url = shutil.copy(p, self.image_dir)
            returned_image_urls.append(image_url)

        # return image URLs
        return returned_image_urls

    def query_images(self, image_urls: List[str]) -> List[str]:
        """
        Given a list of image URLs, return the valid image URLs that exist in storage.
        """
        # Remove None
        valid_image_urls = [url for url in image_urls if url]

        # Check if image exists in storage
        existing_image_urls = [url for url in valid_image_urls if os.path.exists(url)]

        return existing_image_urls
    
    def clear_storage(self):
        if os.path.exists(self.image_dir):
            shutil.rmtree(self.image_dir)
            os.mkdir(self.image_dir)
