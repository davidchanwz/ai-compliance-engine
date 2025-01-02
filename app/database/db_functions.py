from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Text, func, insert, delete
from dotenv import load_dotenv
import os

load_dotenv()

# Fetch database credentials
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# Database setup
engine = create_engine(DATABASE_URL)
metadata = MetaData()


def create_table(table_name: str, columns: list):
    """
    Creates a table in the database.
    :param table_name: Name of the table
    :param columns: List of columns (Column objects)
    """
    table = Table(table_name, metadata, *columns)
    metadata.create_all(engine)
    log_change('CREATE', table_name)
    return table

def delete_table(table_name: str):
    """
    Deletes a table from the database.
    :param table_name: Name of the table to delete
    """
    table = Table(table_name, metadata, autoload_with=engine)
    table.drop(engine)

def add_entry(table_name: str, data: dict):
    """
    Adds an entry to a table.
    :param table_name: Name of the table
    :param data: Dictionary of data to insert
    """
    table = Table(table_name, metadata, autoload_with=engine)
    with engine.connect() as connection:
        connection.execute(insert(table).values(data))
        connection.commit() 
    log_change('INSERT', table_name, data)

def delete_entry(table_name: str, condition: dict):
    """
    Deletes an entry from a table based on a condition = {column : value}
    :param table_name: Name of the table
    :param condition: Dictionary with condition for deletion
    """
    table = Table(table_name, metadata, autoload_with=engine)
    with engine.connect() as connection:
        # Construct WHERE clause
        where_clauses = [table.c[column] == value for column, value in condition.items()]
        connection.execute(delete(table).where(*where_clauses))
        connection.commit()
    log_change('DELETE', table_name, condition)


# logging_utils.py
import datetime
import logging

# Configure logging
logging.basicConfig(filename='database_changes.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def log_change(table_name: str, action: str, data: dict):
    changes_table = Table("database_changes", metadata, autoload_with=engine)

    # Ensure the timestamp is in ISO format (string) if it's present
    if 'timestamp' in data and isinstance(data['timestamp'], datetime.datetime):
        data['timestamp'] = data['timestamp'].isoformat()

    with engine.connect() as connection:
        connection.execute(insert(changes_table).values({
            "table_name": table_name,
            "action": action,
            "data": data,
            "created_at": func.now()  # Using CURRENT_TIMESTAMP
        }))
        connection.commit()