import sqlite3

DEFAULT_DB = "prod.db"

def get_connection(db_path=DEFAULT_DB):
    """
    This function will create connection object from sqlite3
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path=DEFAULT_DB):
    """
    Initialize the SQLite database with required tables.
    """
    conn = get_connection(db_path)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll_no TEXT UNIQUE NOT NULL,
        age INTEGER,
        course TEXT,
        gpa REAL,
        created_at TEXT DEFAULT (datetime('now'))
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS internships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT,
        location TEXT,
        duration TEXT,
        stipend TEXT,
        description TEXT,
        application_deadline TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        internship_id INTEGER NOT NULL,
        applied_at TEXT DEFAULT (datetime('now')),
        status TEXT DEFAULT 'Applied',
        note TEXT,
        FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
        FOREIGN KEY (internship_id) REFERENCES internships(id) ON DELETE CASCADE,
        UNIQUE(student_id, internship_id)
    );
    """)

    conn.commit()
    conn.close()
