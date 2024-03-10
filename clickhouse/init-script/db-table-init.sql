CREATE DATABASE IF NOT EXISTS dev;

CREATE TABLE IF NOT EXISTS dev.kafka_message_log
(
    timestamp UInt64,
    kafka_message String
)
ENGINE = MergeTree()
PRIMARY KEY (timestamp);

CREATE TABLE IF NOT EXISTS dev.invoice
(
    order_id UInt64,
    invoice_number UInt64
)
ENGINE = MergeTree()
PRIMARY KEY (order_id);