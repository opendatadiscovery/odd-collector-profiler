FROM python:3.9.12-slim-buster AS python
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

# For pyodbc
ENV ACCEPT_EULA=Y
RUN apt-get install -y gnupg2

RUN curl -s -o microsoft.asc https://packages.microsoft.com/keys/microsoft.asc \
    && curl -s -o mssql-release.list https://packages.microsoft.com/config/debian/10/prod.list \
    && apt-get install -y g++ unixodbc-dev

RUN apt-key add microsoft.asc && rm microsoft.asc && mv mssql-release.list /etc/apt/sources.list.d/mssql-release.list
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update -y
RUN apt-get install -y msodbcsql18
RUN apt-get install -y mssql-tools18
RUN echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-dev -vvv

COPY odd_collector_profiler ./odd_collector_profiler
COPY collector_config.yaml ./

RUN useradd --create-home --shell /bin/bash app
USER app
COPY start.sh ./start.sh

ENTRYPOINT ["/bin/bash", "start.sh"]