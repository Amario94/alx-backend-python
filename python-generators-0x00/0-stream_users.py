import mysql.connector

def stream_users():
    """Generator that yields rows from user_data one by one."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Change to your actual MySQL password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass

if __name__ == "__main__":
    for user in stream_users():
        print(user)
