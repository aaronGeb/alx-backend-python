#!/usr/bin/env python3

from seed import connect_db

def stream_user_ages():
    """Prints average  ages from the database."""
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT age FROM user_data;")
        for age in cursor:
            yield age[0]


def average_ages():
    """Prints average ages from the database."""
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    if count == 0:
        return 0
    return total_age / count
