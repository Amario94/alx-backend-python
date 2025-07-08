import time
import sqlite3 
import functools

# ✅ Global query cache dictionary
query_cache = {}

# ✅ DB connection decorator
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper_with_db_connection(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper_with_db_connection

# ✅ Query result caching decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper_cache_query(conn, *args, **kwargs):
        # Get SQL query string from args or kwargs
        query = kwargs.get("query", args[0] if args else None)
        if query in query_cache:
            print("[CACHE] Using cached result.")
            return query_cache[query]
        print("[DB] Executing and caching query.")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper_cache_query

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# ✅ First call: fetches from DB and caches
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# ✅ Second call: uses cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
