# App initialization
import os
from typing import Optional
from flask import Flask, render_template, send_from_directory
from pydantic_settings import BaseSettings
import logging
from app.core.config import Settings
from app.models.model_loader import load_image_encoder
from app.db.vector_db_loader import load_vector_db
from app.db.image_storage import ImageStorage
from app.services.search import SearchService
from app.services.indexing import IndexService
from app.api.search_endpoint import SearchEndpoint
from app.api.index_endpoint import IndexEndpoint

def create_app(settings: Optional[BaseSettings]=None) -> Flask:
    if settings is None:
        settings = Settings() # default settings

    # Init Flask app instance
    app = Flask(
        __name__, 
        template_folder=settings.template_dir,
        static_folder=settings.static_dir,
        ) # NOTE: change to "visual-search" package name?

    # Config upload folder
    app.config['UPLOAD_FOLDER'] = settings.upload_dir
    # Create upload folder
    if not os.path.exists(settings.upload_dir):
        os.makedirs(settings.upload_dir)

    # Limit upload file size
    app.config['MAX_CONTENT_LENGTH'] = settings.max_content_length

    # Set env var 'TORCH_HOME' to cache pre-trained weights
    os.environ['TORCH_HOME'] = settings.pre_trained_weights_cache_dir
    if not os.path.exists(settings.pre_trained_weights_cache_dir):
        os.makedirs(settings.pre_trained_weights_cache_dir)


    # Load ML model
    image_encoder, image_process = load_image_encoder(
        settings.device
    )

    # Init database and image storage
    vector_db = load_vector_db(
        database_name=settings.vector_db_name,
        dimension=settings.vector_db_dimension,
        distance=settings.vector_db_distance,
        location=settings.vector_db_location,
    )

    image_storage = ImageStorage(
        image_dir=settings.image_storage_dir,
    )

    # Init services
    search_service = SearchService(
        vector_db=vector_db,
        image_storage=image_storage,
        image_encoder=image_encoder,
        image_process=image_process,
        device=settings.device,
    )

    index_service = IndexService(
        vector_db=vector_db,
        image_storage=image_storage, 
        image_encoder=image_encoder, 
        image_process=image_process,
        device=settings.device,
    )

    # Register API endpoints
    search_endpoint = SearchEndpoint(
        upload_dir=settings.upload_dir,
        search_service=search_service,
        top_k=settings.top_k,
    )
    # Route search request to search_endpoint
    search_endpoint.register_router(app)

    index_endpoint = IndexEndpoint(
        index_service=index_service,
        batch_size=settings.batch_size,
        parallel=settings.parallel,
    )

    # Route indexing request to search_endpoint
    index_endpoint.register_router(app)

    # Route home page
    @app.route('/')
    def index():
        return render_template(
            'index.html'
        )
    
    @app.route('/data/image_storage/<path:filename>')
    def serve_image(filename):
        return send_from_directory(settings.image_storage_file_location, filename)
    
    return app


if __name__ == '__main__':
    app = create_app()

    app.run(
        debug=False,
        use_reloader=False,
        use_debugger=False, 
        threaded=True,
    )