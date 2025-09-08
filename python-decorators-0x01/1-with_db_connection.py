#!/usr/bin/env python3
import sqlite3 
import functools

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
          conn = sqlite3.connect('users.db')
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
 
@with_db_connection 
def get_user_by_id(conn, user_id): 
cursor = conn.cursor() 
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
return cursor.fetchone() 
#### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)