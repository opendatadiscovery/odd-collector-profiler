FROM python:3.9.16 AS python
ENV PYTHONUNBUFFERED=true
ENV PATH=$PATH:/root/.local/bin
WORKDIR /app

FROM python AS build
RUN apt-get update && \
    apt-get install -y \
    curl \
    libpq-dev \
    gcc \
    unixodbc \
    unixodbc-dev \
    g++ \
    python-dev \
    python3-dev

# For pyodbc
ENV ACCEPT_EULA=Y
RUN apt-get install -y gnupg2

RUN curl -s -o microsoft.asc https://packages.microsoft.com/keys/microsoft.asc \
    && curl -s -o mssql-release.list https://packages.microsoft.com/config/debian/10/prod.list \
    && apt-get install -y g++

RUN apt-key add microsoft.asc && rm microsoft.asc && mv mssql-release.list /etc/apt/sources.list.d/mssql-release.list
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update -y
RUN apt-get install -y msodbcsql18
RUN apt-get install -y mssql-tools18
RUN echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc


RUN curl -sSL https://install.python-poetry.org | python3 -
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
COPY . .

RUN pip install --upgrade pip
RUN poetry install --no-interaction --only main


FROM python as runtime
RUN useradd --create-home --shell /bin/bash app
USER app
COPY --from=build /app /app

ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT ["/bin/bash", "start.sh"]