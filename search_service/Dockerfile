# Build in project root
FROM python:3.12.7-slim

WORKDIR /search_service

RUN pip install poetry && \
    poetry config virtualenvs.create false

COPY search_service/pyproject.toml ./
COPY shared_contracts shared_contracts
RUN poetry lock && poetry install --no-root --no-interaction

COPY search_service/app ./app
RUN poetry lock && poetry install --only-root --no-interaction

CMD ["poetry", "run", "python", "-m", "app.main"]