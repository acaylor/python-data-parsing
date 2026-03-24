import sqlite3
import pandas as pd
from sqlite3 import Error
import sys
import argparse

# Function to create a connection to the SQLite database
def create_connection():
    conn = None
    try:
        # Create a new SQLite connection or open an existing one
        conn = sqlite3.connect('workouts.db')
        print("sqlite database version:" + sqlite3.version)
        print("connected to database")
    except Error as e:
        print(e)
    finally:
        if conn:
            return conn

# Function to crate an appropriate database table
def create_table(conn):
    # Create the table
    conn.execute("""
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        start_time DATETIME,
        end_time DATETIME,
        description TEXT,
        exercise_title TEXT,
        superset_id INTEGER,
        exercise_notes TEXT,
        set_index INTEGER,
        set_type TEXT,
        weight_lbs REAL,
        reps INTEGER,
        distance_miles REAL,
        duration_seconds INTEGER,
        rpe INTEGER
    );
    """)
    print("Table created successfully")

# Function to convert CSV to SQLite
def csv_to_sqlite(csv_file, table_name):
    # Create connection to the database
    conn = create_connection()

    # Read CSV file into pandas DataFrame
    df = pd.read_csv(csv_file, parse_dates=["start_time", "end_time"])
    # This assumes that the csv_file has dates in the columns for start_time and end_time

    # Convert empty strings to None (NULL in SQL)
    df = df.where(pd.notnull(df), None)

    # Create the database table
    create_table(conn)

    # Write DataFrame to SQLite database
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    # Close the connection
    conn.close()

# Create argument parser
parser = argparse.ArgumentParser()
parser.add_argument("csv_file", help="The CSV file to convert")
args = parser.parse_args()

# Call function with supplied CSV file and table name as arguments
csv_to_sqlite(args.csv_file, 'workouts')
print("operation completed")
