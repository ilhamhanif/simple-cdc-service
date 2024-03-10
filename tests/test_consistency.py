import unittest


def mysql_client():

    """Fn: Create Connection to MySQL"""

    import mysql.connector
    conn = mysql.connector.connect(
        user='root', 
        password='root',
        host='localhost',
        port=3306,
        database='dev'
    )
    cursor = conn.cursor()

    return conn, cursor


def clickhouse_client():

    """Fn: Create Connection to ClickHouse"""

    import clickhouse_connect
    client = clickhouse_connect.get_client(
        host='localhost', 
        username='default',
        database='dev', 
        port=8123
    )

    return client


class test_consistency(unittest.TestCase):

    def test_row_count(self):

        mysql_query = f"SELECT COUNT(*) row_cnt FROM dev.invoice"
        clickhouse_query = f"SELECT COUNT(*) row_cnt FROM dev.invoice"

        _, mysql_cursor = mysql_client()
        ch_conn = clickhouse_client()

        mysql_cursor.execute(mysql_query)
        for row_cnt in mysql_cursor.fetchone():
            mysql_row_cnt = row_cnt

        result = ch_conn.command(clickhouse_query)
        ch_row_cnt = result

        assert mysql_row_cnt == ch_row_cnt


    def test_each_row(self):

        mysql_query = f"SELECT order_id, invoice_number FROM dev.invoice ORDER BY order_id ASC"
        clickhouse_query = f"SELECT order_id, invoice_number FROM dev.invoice ORDER BY order_id ASC"

        _, mysql_cursor = mysql_client()
        ch_conn = clickhouse_client()

        mysql_cursor.execute(mysql_query)
        list_mysql_res = []
        for (order_id, invoice_number) in mysql_cursor.fetchall():
            list_mysql_res.append({"order_id": order_id, "invoice_number": invoice_number})

        result = ch_conn.query(clickhouse_query)
        list_ch_res = []
        for row in result.result_rows:
            list_ch_res.append({"order_id": row[0], "invoice_number": row[1]})

        for i in range(len(list_mysql_res)):
            assert list_ch_res[i] == list_mysql_res[i]