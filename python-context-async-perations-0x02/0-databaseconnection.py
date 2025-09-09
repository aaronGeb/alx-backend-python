#!/usr/bin/env python3

import sqlite3


class DatabaseConnection:
    """A simple database connection context manager."""

    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        # open connection
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        print("Connection established.", self.db_name)
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.commit()
            self.connection.close()
            print("Connection closed.")
        if exc_type:
            print(f"An error occurred: {exc_value}")
        return False  # Propagate exception if any


if __name__ == "__main__":
    db_name = "../python-decorators-0x01/test_users.db"
    with DatabaseConnection(db_name) as cursor:
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        print("query result:")
        for row in rows:
            print(row)
