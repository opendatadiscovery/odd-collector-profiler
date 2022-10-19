FROM python:3.9.12-slim-buster AS python
ENV PATH=$PATH:/root/.local/bin
WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    curl \
    libpq-dev \
    gcc

RUN curl -sSL https://install.python-poetry.org | python3 -

FROM python AS build
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-dev -vvv

COPY odd_collector_profiler ./odd_collector_profiler
COPY collector_config.yaml ./

RUN useradd --create-home --shell /bin/bash app
USER app
COPY start.sh ./start.sh

ENTRYPOINT ["/bin/bash", "start.sh"]