# ODD Collector Profiler
___

## Description

Reads batch of data and uses [DataProfiler](https://github.com/capitalone/DataProfiler) for getting statistics and map them to DataEntities statistics.





## Implemented profilers

* Postgres

## Config example


| Key                          | Value                                                                             |
| ---------------------------- | --------------------------------------------------------------------------------- |
| **default_pulling_interval** | Once per interval collector will collect statistics and send them to ODD Platform |
| **token**                    | Token created during collector registration via UI or programmatically            |
| **platform_host_url**        | ODD Platform host                                                                 |
| **profilers**                | List of configs for datasources profilers                                         |

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

