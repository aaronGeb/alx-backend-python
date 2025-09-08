#!/usr/bin/env python3
import sqlite3
import csv
from functools import wraps


def with_db_connection(db_path="test_users.db"):
    """Decorator that manages SQLite connection and closes after use."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            conn = None
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                result = func(*args, conn=conn, cursor=cursor, **kwargs)
                conn.commit()
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


@with_db_connection("test_users.db")
def setup_database(conn=None, cursor=None):
    """Create the users table if it doesn’t exist."""
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            age INTEGER
        )
    """
    )
    print("Users table created.")


@with_db_connection("test_users.db")
def load_csv_to_db(csv_file, conn=None, cursor=None):
    """Load user data from CSV into the users table."""
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                cursor.execute(
                    "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                    (row["name"], row["email"], row["age"]),
                )
            except sqlite3.IntegrityError:
                
                pass
    print(f"Data loaded from {csv_file}")


@with_db_connection("test_users.db")
def get_all_users(conn=None, cursor=None):
    """Fetch all users from DB."""
    cursor.execute("SELECT id, name, email, age FROM users")
    return cursor.fetchall()


if __name__ == "__main__":
    setup_database()
    load_csv_to_db("../data/user_data.csv")

    # Print out loaded users
    users = get_all_users()
    print("\nUsers in database:")
    for u in users:
        print(u)
