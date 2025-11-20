# Build in project root
FROM python:3.12.7-slim

WORKDIR /entry_point

RUN pip install poetry && \
    poetry config virtualenvs.create false

COPY entry_point/pyproject.toml ./
COPY shared_contracts shared_contracts
RUN poetry lock && poetry install --no-root --no-interaction

COPY entry_point/app ./app
COPY entry_point/openapi_server ./openapi_server
RUN poetry lock && poetry install --only-root --no-interaction

CMD ["poetry", "run", "gunicorn", "openapi_server.__main__:create_app()", "-b", "0.0.0.0:8000", "-w", "1", "--preload", "--timeout", "120", "--max-requests", "1000"]