FROM pytorch/pytorch:2.8.0-cuda12.8-cudnn9-runtime

WORKDIR /visual-search

# Install Poetry
RUN pip install poetry && poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
# Install dependencies without dev dependencies
RUN poetry install --no-root --no-interaction --only main 

# Install application
COPY app/ ./app
RUN poetry install --no-interaction --only-root

# Runtime command
CMD ["poetry", "run", "gunicorn", "app.main:create_app()", "-b", "0.0.0.0:8000", "-w", "1", "--preload", "--timeout", "120", "--max-requests", "1000"]

