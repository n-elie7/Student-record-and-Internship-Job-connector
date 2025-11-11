import sqlite3

from database import DEFAULT_DB, get_connection


def add_internship(title, company, location, duration, stipend, description, deadline, db_path=DEFAULT_DB):
    conn = get_connection(db_path)
    cur = conn.cursor() # creates cursor
