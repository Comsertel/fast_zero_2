FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR app/
COPY . .

RUN pip install poetry

RUN apt-get update && apt-get install -y \
    build-essential python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN pip install --no-binary :all: --compile psutil

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi
RUN pip install "fastapi[standard]"

EXPOSE 8000
CMD poetry run uvicorn --host 0.0.0.0 fast_zero.app:app
