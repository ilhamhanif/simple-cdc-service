import mysql.connector
import random


def insert(value):

    """Fn: Return Insert Query with value input"""
    return f"INSERT INTO dev.invoice (order_id, invoice_number) VALUES ({value}, {value})"

def delete(value):

    """Fn: Return Delete Query with value input"""
    return f"DELETE FROM dev.invoice WHERE order_id = {value}"

def update(value):
    
    """Fn: Return Update Query with value input"""
    return f"UPDATE dev.invoice SET invoice_number = {value + 1} where order_id = {value}"

def truncate():

    """Fn: Return Truncate Query"""
    return f"TRUNCATE TABLE dev.invoice"

def main() -> None:

    # Make connection to MySQL in localhost:3306
    conn = mysql.connector.connect(
        user='root', 
        password='root',
        host='localhost',
        port=3306,
        database='dev'
    )
    cursor = conn.cursor()

    # Clean Table
    cursor.execute(truncate())
    conn.commit()

    # Start the Sequencer
    loop = 1800
    list_seq_count = int(loop/3) # For 3 methods.

    list_seq_insert = [random.randint(0, loop) for _ in range (list_seq_count)]
    list_seq_delete = [random.randint(0, loop) for _ in range (list_seq_count)]
    list_seq_update = [random.randint(0, loop) for _ in range (list_seq_count)]

    for v in range (loop):
        value = v

        try:
            if value in list_seq_insert:
                cursor.execute(insert(value))
                status = "OK"
                method = "INSERT"
            elif value in list_seq_delete:
                cursor.execute(insert(value))
                status = "OK"
                method = "DELETE"
            elif value in list_seq_update:
                cursor.execute(insert(value))
                status = "OK"
                method = "UPDATE"
            else:
                status = "FAIL"
                method = "UNKNOWN"
            conn.commit()
        except:
            status = "FAIL"
            method = "UNKNOWN"
            
        finally:
            if status == "OK":
                print(value, status, method)
            else:
                pass
            
    cursor.close()
    conn.close()



if __name__ == "__main__":
    _ = main()