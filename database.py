import sqlite3

DEFAULT_DB = "prod.db"

def get_connection(db_path=DEFAULT_DB):
    """
    This function will create connection object from sqlite3
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
