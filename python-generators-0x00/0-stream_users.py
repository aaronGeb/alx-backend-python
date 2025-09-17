#!/usr/bin/env python3
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


def stream_users():
    """Stream all users in the database"""
    db = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
    )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user_data")
    for row in cursor.fetchall():
        yield row
    cursor.close()
    db.close()
