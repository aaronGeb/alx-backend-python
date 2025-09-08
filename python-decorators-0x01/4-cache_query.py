import time
import sqlite3
import functools


"""your code goes here"""


def with_db_connection(func):
    """
    Decorator that opens a DB connection, passes it to the function,
    and closes it afterwards.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            conn = None
            try:
                # Open a database connection
                conn = sqlite3.connect("users.db")
                cursor = conn.cursor()
                # pass the connection to the decorated function
                result = func(*args, conn=conn, cursor=cursor, **kwargs)
                conn.commit()  # Commit any changes if needed
                return result
            except Exception as e:
                if conn:
                    conn.rollback()
                raise e
            finally:
                if conn:
                    conn.close()

        return wrapper

    return decorator


def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query_cache = {}
        query = kwargs.get("query", "") or (args[1] if len(args) > 1 else "")
        if query in query_cache:
            print("Using cached result for query.")
            return query_cache[query]
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result

    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
