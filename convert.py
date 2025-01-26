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
        conn = sqlite3.connect('strong.db')
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            return conn

# Function to convert CSV to SQLite
def csv_to_sqlite(csv_file, table_name):
    # Create connection to the database
    conn = create_connection()

    # Read CSV file into pandas DataFrame
    df = pd.read_csv(csv_file)

    # Write DataFrame to SQLite database
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    # Close the connection
    conn.close()

# Create argument parser
parser = argparse.ArgumentParser()
parser.add_argument("csv_file", help="The CSV file to convert")
args = parser.parse_args()

# Call function with supplied CSV file and table name as arguments
csv_to_sqlite(args.csv_file, 'strong')
