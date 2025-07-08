import time
import sqlite3 
import functools

# ✅ Decorator to open and close DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper_with_db_connection(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper_with_db_connection

# ✅ Decorator to retry function on failure
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    print(f"[Attempt {attempt}] Trying operation...")
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Error on attempt {attempt}: {e}")
                    last_exception = e
                    time.sleep(delay)
            print(f"All {retries} retries failed.")
            raise last_exception
        return wrapper_retry
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# ✅ Attempt to fetch users with retry mechanism
users = fetch_users_with_retry()
print(users)
