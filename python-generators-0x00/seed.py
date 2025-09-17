#!/usr/bin/env python3
import os
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import csv
import uuid

# Load environment variables
load_dotenv()


def connect_db():
    """connect to mysql server"""
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
    )


def create_database(connection):
    """create database"""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)
    finally:
        cursor.close()


def connect_to_prodev():
    """connect to ALX_prodev database"""
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database="ALX_prodev",
        port=int(os.getenv("MYSQL_PORT")),
    )


def create_table(connection):
    """create users table"""
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
       user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        age DECIMAL NOT NULL,
        INDEX (user_id)
    )
    """
    try:
        cursor.execute(create_table_query)
        print("Table created successfully")
    except mysql.connector.Error as err:
        print("Failed creating table:", err)
    finally:
        cursor.close()


def insert_data(connection, data):
    """insert data into users table"""
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.executemany(insert_query, data)
        connection.commit()
        print(f"{cursor.rowcount} records inserted successfully")
    except mysql.connector.Error as err:
        print("Failed inserting data:", err)
    finally:
        cursor.close()


def load_csv_data(file_path):
    """load data from CSV file"""
    data = []
    with open(file_path, newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append((str(uuid.uuid4()), row["name"], row["email"], row["age"]))
    return data


if __name__ == "__main__":
    # Step 1: Connect to server and create DB
    conn = connect_db()
    create_database(conn)
    conn.close()

    # Step 2: Connect to ALX_prodev and set up table
    conn = connect_to_prodev()
    create_table(conn)

    # Step 3: Load CSV and insert data
    csv_data = load_csv_data("../data/user_data.csv")
    insert_data(conn, csv_data)

    conn.close()
    print("Seeding completed")
