import csv
import uuid
import mysql.connector
from mysql.connector import errorcode


def connect_db():
    """Connect to the MySQL server (not to a specific database yet)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""  # <- change this to your MySQL root password
        )
        print("Connected to MySQL server.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_database(connection):
    """Create ALX_prodev database if it doesn't exist."""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev ensured.")
    except mysql.connector.Error as err:
        print(f"Database creation failed: {err}")
    finally:
        cursor.close()


def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # <- change this to your MySQL root password
            database="ALX_prodev"
        )
        print("Connected to ALX_prodev database.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_table(connection):
    """Create user_data table if it doesn't exist."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX(email)
    )
    """
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_query)
        print("Table user_data ensured.")
    except mysql.connector.Error as err:
        print(f"Table creation failed: {err}")
    finally:
        cursor.close()


def insert_data(connection, data):
    """Insert a row if the email does not already exist."""
    cursor = connection.cursor()
    check_query = "SELECT user_id FROM user_data WHERE email = %s"
    insert_query = "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
    try:
        for row in data:
            name, email, age = row
            cursor.execute(check_query, (email,))
            result = cursor.fetchone()
            if result:
                print(f"Skipping duplicate email: {email}")
                continue
            user_id = str(uuid.uuid4())
            cursor.execute(insert_query, (user_id, name, email, age))
        connection.commit()
        print("Data inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Insertion error: {err}")
    finally:
        cursor.close()


def read_csv(filepath):
    """Read user_data.csv and return list of rows excluding headers."""
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header
        return [row for row in reader]


if __name__ == "__main__":
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()

    db_conn = connect_to_prodev()
    if db_conn:
        create_table(db_conn)
        data = read_csv("user_data.csv")
        insert_data(db_conn, data)
        db_conn.close()
