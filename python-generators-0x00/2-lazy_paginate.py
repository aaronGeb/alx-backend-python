#!/usr/bin/python3
from seed import connect_db

def paginate_users(page_size, offset):
    """Generator function to yield users in pages"""
    cursor = connect_db.cursor()
    cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
    rows = cursor.fetchall()
    for row in rows:
        yield row


def lazy_paginate(page_size):
    """Lazy pagination function"""
    offset = 0
    while True:
        users = paginate_users(page_size, offset)
        for user in users:
            yield user
        offset += page_size
        if offset >= 1000:  # total of 1000 users
            break
