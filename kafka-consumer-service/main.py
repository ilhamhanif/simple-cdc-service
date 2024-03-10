import clickhouse_connect
from clickhouse_connect.driver.client import Client
from clickhouse_connect.driver.summary import QuerySummary
from clickhouse_connect.driver.query import QueryResult
from kafka import KafkaConsumer
import json


def ch_query_data(client: Client, query: str, **kwargs) -> QueryResult:

    """Fn: Query to ClickHouse"""
    return client.query(query, **kwargs)

def ch_insert_data(client: Client, table_name: str, data: list, column_names: list) -> QuerySummary:

    """Fn: Insert Data to ClickHouse"""
    return client.insert(table_name, data, column_names=column_names)


def main() -> None:

    """Fn: Main"""

    # Setup a KafkaConsumer
    kafka_consumer = KafkaConsumer(
        bootstrap_servers=['kafka:29093'], 
        auto_offset_reset='latest',
    )
    kafka_consumer.subscribe(topics=['source.dev.invoice'])

    # Setup a ClickHouse Client
    clickhouse_client = clickhouse_connect.get_client(host='clickhouse', username='default', database='dev', port=8123)

    for m in kafka_consumer:
        timestamp = m.timestamp
        value = m.value
        if not value: # DELETE is pushing None value records
            continue
        else:
            pass

        # Insert all Message to a Table
        message = json.loads(value.decode("utf-8"))
        data = [[timestamp, json.dumps(message)]]
        _ = ch_insert_data(clickhouse_client, "dev.kafka_message_log", data, ["timestamp", "kafka_message"])

        # Sync ClicHouse Table with Source Table
        # Currently Response for INSERT, UPDATE, DELETE (including TRUNCATE) on TABLE EVENT
        if message["payload"]["before"] is None and message["payload"]["after"] is not None: # Insert
            data = message["payload"]["after"]
            data = [[v for _, v in data.items()]]
            _ = ch_insert_data(clickhouse_client, "dev.invoice", data, ["order_id", "invoice_number"])

        elif message["payload"]["before"] is not None and message["payload"]["after"] is not None: # Update
            data_after = message["payload"]["after"]
            query_update = ""
            ch_primary_key_column = "order_id"
            for i, (column_name, column_value) in enumerate(data_after.items()):
                if column_name != ch_primary_key_column:
                    query_update += " "
                    query_update += f"{column_name} = {column_value}"
                else:
                    continue

            data_before = message["payload"]["before"]
            query_filter = "WHERE"
            for i, (column_name, column_value) in enumerate(data_before.items()):
                if column_name == ch_primary_key_column:
                    query_filter += " "
                    query_filter += f"{column_name} = {column_value}"

            query = f"""ALTER TABLE dev.invoice UPDATE {query_update} {query_filter}"""
            _ = ch_query_data(clickhouse_client, query)

        elif message["payload"]["before"] is not None and message["payload"]["after"] is None: # Delete
            data = message["payload"]["before"]
            query_filter = "WHERE"
            for i, (column_name, column_value) in enumerate(data.items()):
                if i == 0:
                    query_filter += " "
                else:
                    query_filter += " " + "AND" + " "
                query_filter += f"{column_name} = {column_value}"

            query = f"""ALTER TABLE dev.invoice DELETE {query_filter}"""
            _ = ch_query_data(clickhouse_client, query)

        elif message["payload"]["before"] is None and message["payload"]["after"] is None: # Truncate
            query = f"""TRUNCATE TABLE dev.invoice"""
            _ = ch_query_data(clickhouse_client, query)

        else:
            print("Unknown Condition.")


if __name__ == "__main__":
    _ = main()