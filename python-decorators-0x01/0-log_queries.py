import sqlite3
import functools

from init_db import initialize_database  # import setup

# Ensure DB is ready
initialize_database()  #  call setup before any query

#### Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper_log_queries(*args, **kwargs):
        query = kwargs.get("query", args[0] if args else None)
        if query:
            print(f"[LOG] Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper_log_queries

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)
