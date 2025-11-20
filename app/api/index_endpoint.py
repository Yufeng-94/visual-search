from flask import Flask, request, jsonify
import os
from app.services.indexing import IndexService

class IndexEndpoint:

    def __init__(
            self, 
            index_service: IndexService, 
            batch_size: int,
            parallel: int,
            ):
        self.index_service = index_service
        self.batch_size = batch_size
        self.parallel = parallel

    def post(self):
        # Input validation and parsing
        if not request.is_json:
            return jsonify({"error": "Invalid input, JSON expected"}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "Input missing"}), 400
        
        image_dir = data.get("image_dir", None)
        metadata_dir = data.get("metadata_dir", None)
        if not image_dir or not metadata_dir:
            return jsonify({"error": "Both 'image_dir' and 'metadata_dir' must be provided"}), 400

        # Authentication: Skipped for simplicity

        # Indexing logic. NOTE: Only for local mode with small scale uploads. Should be replaced with async job queue for production use.
        try:
            # List all files in the directory
            upload_image_paths = os.listdir(image_dir)
            upload_image_paths = [os.path.join(image_dir, p) for p in upload_image_paths]
            upload_metadata_paths = os.listdir(metadata_dir)
            upload_metadata_paths = [os.path.join(metadata_dir, p) for p in upload_metadata_paths]

            # Upload images and metadata
            self.index_service.index_images(
                image_paths = upload_image_paths,
                metadata_paths = upload_metadata_paths,
                batch_size=self.batch_size,
                parallel=self.parallel,
            )

            return jsonify({"message": "Indexing completed"}), 200

        except Exception as e:
            return jsonify({"error": f"Failed to list files in directory: {e}"}), 500

    def register_router(self, app: Flask):
        app.add_url_rule(
            '/index', 
            view_func=self.post, 
            methods=['POST'], 
            endpoint='index_endpoint'
            )
