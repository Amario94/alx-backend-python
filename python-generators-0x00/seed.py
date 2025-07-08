#!/usr/bin/python3
import mysql.connector
import csv
import uuid

# 1. Connects to MySQL server (no database yet)
def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='dMPXVti9W8r@cpx'  # 👈 replace this
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

# 2. Creates ALX_prodev database if it doesn't exist
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
        print("Database ALX_prodev created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

# 3. Connects to the ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='dMPXVti9W8r@cpx',  # 👈 replace this too
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

# 4. Creates the user_data table if it doesn't exist
def create_table(connection):
    try:
        cursor = connection.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX (user_id)
        )
        """
        cursor.execute(query)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

# 5. Inserts data from CSV into the table
def insert_data(connection, csv_filename):
    try:
        cursor = connection.cursor()
        with open(csv_filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, name, email, age))
        connection.commit()
        cursor.close()
        print(f"Data inserted from {csv_filename}")
    except Exception as err:
        print(f"Error inserting data: {err}")

