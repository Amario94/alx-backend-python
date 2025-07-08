# import sqlite3
# import functools
# from datetime import datetime


# from init_db import initialize_database  # import setup

# # Ensure DB is ready
# initialize_database()  #  call setup before any query

# #### Decorator to log SQL queries
# def log_queries(func):
#     @functools.wraps(func)
#     def wrapper_log_queries(*args, **kwargs):
#         query = kwargs.get("query", args[0] if args else None)
#         if query:
#             print(f"[LOG] Executing SQL Query: {query}")
#         return func(*args, **kwargs)
#     return wrapper_log_queries

# @log_queries
# def fetch_all_users(query):
#     conn = sqlite3.connect('users.db')
#     cursor = conn.cursor()
#     cursor.execute(query)
#     results = cursor.fetchall()
#     conn.close()
#     return results

# #### Fetch users while logging the query
# users = fetch_all_users(query="SELECT * FROM users")
# print(users)

import sqlite3
import functools
from datetime import datetime  #  Add this line

from init_db import initialize_database  # Ensure DB setup

# Initialize DB before any operation
initialize_database()

#  Decorator to log SQL queries with timestamp
def log_queries(func):
    @functools.wraps(func)
    def wrapper_log_queries(*args, **kwargs):
        query = kwargs.get("query", args[0] if args else None)
        if query:
            print(f"[{datetime.now()}] Executing SQL Query: {query}")
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

# Fetch and log query
users = fetch_all_users(query="SELECT * FROM users")
print(users)
