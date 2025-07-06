import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that fetches user data from the database in batches of `batch_size`.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Replace with your MySQL password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)

        offset = 0
        while True:
            cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset))
            rows = cursor.fetchall()
            if not rows:
                break
            yield rows
            offset += batch_size

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass


def batch_processing(batch_size):
    """
    Generator that processes batches and yields users over age 25.
    """
    for batch in stream_users_in_batches(batch_size):  # loop 1
        filtered = [user for user in batch if float(user['age']) > 25]  # loop 2 (internally in list comp)
        yield filtered  # Yield entire filtered batch (list of users)


# Optional example usage:
if __name__ == "__main__":
    for filtered_batch in batch_processing(5):  # loop 3
        for user in filtered_batch:
            print(user)
