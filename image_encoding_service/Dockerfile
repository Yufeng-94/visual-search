FROM pytorch/pytorch:2.8.0-cuda12.8-cudnn9-runtime

WORKDIR /image_encoding_service

RUN pip install poetry && \
    poetry config virtualenvs.create false

COPY image_encoding_service/pyproject.toml .
COPY shared_contracts ./shared_contracts
RUN poetry lock && poetry install --no-interaction --no-root

COPY image_encoding_service/app ./app
RUN poetry lock && poetry install --no-interaction --only-root

CMD ["poetry", "run", "python", "-m", "app.main"]