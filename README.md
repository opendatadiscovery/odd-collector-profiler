# ODD Collector Profiler

Reads batch of data and uses [DataProfiler](https://github.com/capitalone/DataProfiler) for getting statistics and map them to ODD DataEntities statistics.

- [ODD Collector Profiler](#odd-collector-profiler)
  - [Supported data sources](#supported-data-sources)
  - [Config example](#config-example)
  - [Docker build](#docker-build)
  - [M1 Issue](#m1-issue)
    - [Pyodbc](#pyodbc)
    - [**grpcio**](#grpcio)
    - [**tensorflow**](#tensorflow)


## Supported data sources
- [x] **Postgres**
- [x] **Azure SQL**

## Config example


| Key                          | Value                                                                             |
| ---------------------------- | --------------------------------------------------------------------------------- |
| **default_pulling_interval** | Once per interval collector will collect statistics and send them to ODD Platform |
| **token**                    | Token created during collector registration via UI or programmatically            |
| **platform_host_url**        | ODD Platform host                                                                 |
| **profilers**                | List of configs for datasources profilers                                         |


`collector-config.yaml`
```yaml
default_pulling_interval: 360
token:  <COLLECTOR_TOKEN>
platform_host_url: http://localhost:8080
profilers:
  - type: postgres
    name: my_postgres
    host: localhost
    port: 5432
    username: postgres
    password: ""
    database: db
    tables: ["some_table"]
```

## Docker build
```bash
docker build . -t odd_collector_profiler
```

## M1 Issue

### Pyodbc
On M1 pyodbc needs to be installed as no-binary. Command below will add that info to `poetry.toml`:
```shell
poetry config --local installer.no-binary pyodbc
```

### **grpcio**
Needs an env variables:
```shell
export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=1
export GRPC_PYTHON_BUILD_SYSTEM_ZLIB=1
```

### **tensorflow**
DataProfiler uses tensorflow package for auto-labeling, there are no ready `.whl` for M1.
Need it to be builded and used manually, read the Tensorflow documentation.
