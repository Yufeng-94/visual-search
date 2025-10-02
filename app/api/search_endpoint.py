from flask import Flask, request, jsonify
import os
from app.services.search import SearchService
from typing import List
import uuid
import time

class SearchEndpoint:

    def __init__(self, upload_dir: str, search_service:SearchService, top_k: int):
        self.upload_dir = upload_dir
        self.search_service = search_service
        self.top_k = top_k

    def post(self):
        # Create search_id
        search_id = str(uuid.uuid4())
        processing_time_start = time.time()

        # Save uploaded image
        uploaded_file_path = self._upload_file()

        # Image search
        retrieved_image_metadata = self._search_image(uploaded_file_path)

        # Remove uploaded image
        os.remove(uploaded_file_path)

        # Return response
        processing_time_ms = (time.time() - processing_time_start) * 1000
        response = self._fetch_response(
            retrieved_image_metadata, 
            search_id, 
            processing_time_ms
            )
        return jsonify(response)

    def register_router(self, app: Flask):
        app.add_url_rule(
            '/upload', 
            view_func=self.post, 
            methods=['POST'], 
            endpoint='search_endpoint',
            )

    def _upload_file(self) -> str:

        # Validate uploaded file
        file = request.files.get('file', None)
        if file is None:
            return jsonify({'error': 'No file provided'}), 400
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        try:
            # Save uploaded file temporarily
            filepath = os.path.join(self.upload_dir, file.filename)
            file.save(filepath)

            return filepath
        except Exception as e:
            return jsonify({'error': f'Failed to save uploaded file: {e}'}), 500
    
    def _search_image(self, uploaded_file_path: str) -> List[dict]:
        
        return self.search_service.search(uploaded_file_path, self.top_k)
    
    def _fetch_response(
            self, 
            retrieved_image_metadata: List[dict], 
            search_id: str, 
            processing_time_ms: int
            ) -> dict:

        return {
            "search_id": search_id,
            "processing_time_ms": processing_time_ms,
            "retrieved_images": retrieved_image_metadata,
        }