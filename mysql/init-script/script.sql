CREATE DATABASE dev;

CREATE TABLE dev.invoice (
    order_id INT NOT NULL,
    invoice_number INT NOT NULL,
    PRIMARY KEY (order_id)
);