# Build in project root
FROM python:3.12.7-slim

WORKDIR /indexing_service

RUN pip install poetry && \
    poetry config virtualenvs.create false

COPY indexing_service/pyproject.toml ./
COPY shared_contracts shared_contracts
RUN poetry lock && poetry install --no-root --no-interaction

COPY indexing_service/app ./app
RUN poetry lock && poetry install --only-root --no-interaction

CMD ["poetry", "run", "python", "-m", "app.main"]