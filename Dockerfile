FROM python:3.9.16-slim AS python
ENV PATH=$PATH:/root/.local/bin
WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    curl \
    libpq-dev \
    gcc \
    unixodbc \
    unixodbc-dev 

RUN curl -sSL https://install.python-poetry.org | python3 -

FROM python AS build
COPY poetry.lock pyproject.toml ./

# For pyodbc
RUN curl -s -o microsoft.asc https://packages.microsoft.com/keys/microsoft.asc \
    && curl -s -o mssql-release.list https://packages.microsoft.com/config/debian/10/prod.list \
    && apt-get update -y \
    && apt-get install -y g++ unixodbc-dev

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-dev -vvv

COPY odd_collector_profiler ./odd_collector_profiler
COPY collector_config.yaml ./

RUN useradd --create-home --shell /bin/bash app
USER app
COPY start.sh ./start.sh

ENTRYPOINT ["/bin/bash", "start.sh"]