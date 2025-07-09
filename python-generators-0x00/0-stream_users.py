#!/usr/bin/python3
import mysql.connector

def stream_users():
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='dMPXVti9W8r@cpx
        database='ALX_prodev'
    )
    cursor = connection.cursor(dictionary=True)

    # Execute the query
    cursor.execute("SELECT * FROM user_data")

    # Yield each row one by one
    for row in cursor:
        yield row

    # Close connection (after generator is fully consumed)
    cursor.close()
    connection.close()
