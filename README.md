# Visual Search System

A scalable microservices-based visual search engine that enables users to search for similar images using deep learning embeddings. The system processes images, extracts visual features, and performs similarity search using vector databases.

## 🏗️ Architecture

The system consists of multiple microservices working together:

![Architecture](docs/images/Untitled%20Diagram.drawio.svg)

### Service Components

- **Entry Point** (`entry-point`): Flask-based REST API gateway that handles HTTP requests and coordinates with backend services
- **Image Encoding Service** (`image-encoding-service`): Extracts visual features from images using deep learning models (PyTorch)
- **Indexing Service** (`indexing-service`): Processes batches of images and stores their embeddings in the vector database
- **Search Service** (`search-service`): Performs similarity search queries against the vector database
- **Infrastructure Services**:
  - **Redis**: Message queue and caching layer
  - **S3 (LocalStack)**: Storage for images and metadata
  - **Qdrant**: Vector database for storing and searching image embeddings
  - **Nginx**: Reverse proxy and load balancer

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- At least 8GB RAM (for ML models)
- CUDA-compatible GPU (optional, for faster encoding)

### 1. Clone and Start Services

```bash
git clone https://github.com/Yufeng-94/visual-search.git
cd visual-search
docker-compose up -d
```

### 2. Wait for Services to Initialize

Check that all services are running:

```bash
docker-compose ps
```

All services should show "Up" status. The image encoding service may take a few minutes to download ML models on first start.

### 3. Index Sample Images

Use the admin tools to index your first batch of images:

```bash
# Index images from S3 buckets
curl -X POST http://localhost/api/index \
  -H "Content-Type: application/json" \
  -d '{
    "image_storage_bucket": "source-image-bucket",
    "metadata_storage_bucket": "source-metadata-bucket"
  }'
```

or run

```bash
cd admin
poetry lock
poetry install
poetry run python -m admin.index_images.py
```
with your own `source-image-bucket` and `source-metadata-bucket`

### 4. Search for Similar Images

Open `http://localhost` in browser and drop or upload query images via the web page.

For development testing:

```bash
# Search using an image file
curl -X POST http://localhost/api/search \
  -F "file=@/path/to/your/image.jpg"
```

## 📋 API Reference

### Index Images

**POST** `/api/index`

Index a batch of images from S3 storage.

```json
{
  "image_storage_bucket": "source-image-bucket",
  "metadata_storage_bucket": "source-metadata-bucket"
}
```

**Response:**
```json
{
  "job_id": "uuid-string",
  "message": "Indexing job started successfully"
}
```

### Search Similar Images

**POST** `/api/search`

Find similar images by uploading an image file.

**Request:** Multipart form with `file` field containing image data

**Response:**
```json
{
  "search_id": "uuid-string",
  "processing_ms": 150,
  "similar_images": [
    {
      "image_url": "s3://bucket/image1.jpg",
      "similarity_score": 0.95
    },
    {
      "image_url": "s3://bucket/image2.jpg", 
      "similarity_score": 0.87
    }
  ]
}
```

## 🛠️ Development

### Local Development Setup

1. **Set up Python environments for each service:**

```bash
# Example for image encoding service
cd search_service
poetry lock
poetry install
eval $(poetry env activate)
```

2. **Start infrastructure services only:**

```bash
# Start only Redis, LocalStack, Qdrant
docker-compose up redis localstack qdrant -d
```

3. **Run services locally:**

```bash
# Terminal 1 - Image Encoding Service
cd image_encoding_service
poetry run python -m app.main

# Terminal 2 - Indexing Service  
cd indexing_service
poetry run python -m app.main

# Terminal 3 - Search Service
cd search_service
poetry run python -m app.main

# Terminal 4 - Entry Point
cd entry_point  
poetry run python -m app.main
```

### Development Tools

The `admin/` directory contains useful scripts:

- **`index_images.py`**: Index images from S3 buckets
- **`search_images.py`**: Test image search functionality
- **`create_infra.py`**: Set up S3 buckets and initial data
- **`remove_infra.py`**: Clean up development resources

### Testing

Each service includes unit and integration tests:

```bash
cd indexing_service
poetry run pytest tests/
```

## 🐳 Docker Images

Pre-built images are available on Docker Hub:

- `yufeng94/vs-entry-point:v1.0`
- `yufeng94/vs-image-encoding-service:v1.0`
- `yufeng94/vs-indexing-service:v1.0`
- `yufeng94/vs-search-service:v1.0`
- `yufeng94/vs-nginx:v1.0`

## 📊 Monitoring

### Service Health Checks

```bash
# Check all services
curl http://localhost:8000/health
```

### Logs

```bash
# View logs for all services
docker-compose logs -f

# View logs for specific service
docker-compose logs -f image-encoding-service
```

For more help, please open an issue on GitHub.