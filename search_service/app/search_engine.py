
class SearchEngine:
    def search(self, image: bytes, max_results: int):
        # Dummy implementation for illustration
        return [
            {
                'image_url': 'http://example.com/image1.jpg',
                'similarity_score': 0.95,
                'width': 800,
                'height': 600,
            },
            {
                'image_url': 'http://example.com/image2.jpg',
                'similarity_score': 0.90,
                'width': 1024,
                'height': 768,
            },
        ][:max_results]