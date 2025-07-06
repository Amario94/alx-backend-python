import mysql.connector

def paginate_users(page_size, offset):
    """
    Fetches a single page of users starting from the given offset.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Update with your MySQL password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))
        rows = cursor.fetchall()
        return rows

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return []

    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass


def lazy_paginate(page_size):
    """
    Generator that lazily paginates the user_data table.
    Fetches one page at a time and yields each row lazily.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        for row in page:
            yield row
        offset += page_size


# Example usage
if __name__ == "__main__":
    print("Streaming users lazily by pages of 3:")
    for user in lazy_paginate(page_size=3):
        print(user)
