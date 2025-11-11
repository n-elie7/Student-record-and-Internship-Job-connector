import sqlite3
from database import DEFAULT_DB, get_connection

def add_student(name, roll_no, age=None, course=None, gpa=None, db_path=DEFAULT_DB):
    """
    Add a student to the database.
    Returns: lastrowid on success.
    Raises ValueError on duplicate roll_no or other integrity errors.
    """
    conn = get_connection(db_path)
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO students (name, roll_no, age, course, gpa) VALUES (?, ?, ?, ?, ?)",
            (name.strip(), roll_no.strip(), age.strip(), course.strip(), gpa.strip())
        )
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Failed to add student: {e}") from e
    finally:
        conn.close()

def get_all_students(db_path=DEFAULT_DB):
    pass

def find_student_by_roll(roll_no, db_path=DEFAULT_DB):
    pass

def search_students_by_name(name_substr, db_path=DEFAULT_DB):
    pass

def update_student(roll_no, db_path=DEFAULT_DB, **fields):
    pass

def delete_student(roll_no, db_path=DEFAULT_DB):
    pass
