import time
import sqlite3
import functools


#### paste your with_db_decorator here
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


def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries a function upon failure.
    :param retries: Number of retry attempts
    :param delay: Delay between retries in seconds
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(
                        f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds..."
                    )
                    time.sleep(delay)
            raise last_exception

        return wrapper

    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)
