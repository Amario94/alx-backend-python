import mysql.connector

def stream_users_in_batches(batch_size):
    """Yields batches of rows from the user_data table."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # change to your MySQL password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        batch = []
        for row in cursor:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []

        if batch:  # yield any remaining rows
            yield batch

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass


def batch_processing(batch_size):
    """Yields only users over age 25 from each batch."""
    for batch in stream_users_in_batches(batch_size):
        yield [user for user in batch if float(user['age']) > 25]


# Example usage
if __name__ == "__main__":
    for filtered_batch in batch_processing(batch_size=3):
        print("Filtered batch:")
        for user in filtered_batch:
            print(user)
