#!/usr/bin/env python3
import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        # Open connection and execute query
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results  # Return results directly

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Commit (if needed) and close connection
        if self.conn:
            self.conn.commit()
            self.conn.close()
        # Do not suppress exceptions
        return False


if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery("../python-decorators-0x01/test_users.db", query, params) as results:
        print("Query Results:")
        for row in results:
            print(row)
