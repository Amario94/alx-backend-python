import mysql.connector

def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_mysql_password",  # replace this!
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)

    offset = 0
    while True:
        cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset))
        batch = cursor.fetchall()
        if not batch:
            break
        yield batch
        offset += batch_size

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                print(user)
