#!/usr/bin/env python3
from seed import connect_db


def stream_users_in_batches(batch_size):
    """Generator function to yield users in batches"""

    cursor = connect_db.cursor()
    cursor.execute("SELECT * FROM user_data")
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        for row in rows:
            yield row

def batch_processing(batch_size):
    """Generator function to yield users in batches"""
    cursor = connect_db.cursor()
    cursor.execute("SELECT * FROM user_data WHERE age > 25")
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            return []
        for row in rows:
          yield row
