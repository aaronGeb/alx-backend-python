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


def transactional(func):
    """
    Decorator that wraps the function in a database transaction.
    Commits the transaction if the function succeeds, rolls back if it fails.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = kwargs.get("conn")
        if conn is None:
            raise ValueError("Database connection not provided to the function.")
        try:
            result = func(*args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e

    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


#### Update user's email with automatic transaction handling

update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")
