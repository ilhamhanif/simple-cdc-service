#!/bin/bash

sleep 10

curl --location 'localhost:8083/connectors' \
--header 'Content-Type: application/json' \
--data '{
    "name": "mysql-schema-dev-connector",  
    "config": {  
      "connector.class": "io.debezium.connector.mysql.MySqlConnector",
      "database.hostname": "mysql",  
      "database.port": "3306",
      "database.user": "root",
      "database.password": "root",
      "database.server.id": "184054",
      "topic.prefix": "source",
      "database.include.list": "dev",
      "skipped.operations": "none",
      "schema.history.internal.kafka.bootstrap.servers": "kafka:9092",  
      "schema.history.internal.kafka.topic": "schema-history.dev",
      "include.schema.changes": "true"
    }
  }' | jq .