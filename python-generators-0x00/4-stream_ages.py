import mysql.connector

def stream_user_ages():
    """
    Generator that yields user ages one by one from the database.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Replace with your MySQL password
            database="ALX_prodev"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")

        for (age,) in cursor:
            yield float(age)

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass


def compute_average_age():
    """
    Computes average age using stream_user_ages generator.
    """
    total_age = 0.0
    count = 0

    for age in stream_user_ages():  # ✅ loop 1
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")


# Run the script
if __name__ == "__main__":
    compute_average_age()
