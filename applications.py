from datetime import date, datetime
import sqlite3
from database import DEFAULT_DB, get_connection


def apply_to_internship(student_roll, internship_id, note=None, db_path=DEFAULT_DB):
    """
    Create an application for a student to an internship.
    Blocks applying after deadline (design choice). Raises ValueError for issues.
    """
    conn = get_connection(db_path)
    cur = conn.cursor()

    cur.execute("SELECT id FROM students WHERE roll_no = ?", (student_roll.strip(),))
    row = cur.fetchone()
    if not row:
        conn.close()
        raise ValueError('Student with that roll number not found')
    student_id = row['id']

    cur.execute("SELECT id, application_deadline FROM internships WHERE id = ?", (internship_id,))
    intern = cur.fetchone()
    if not intern:
        conn.close()
        raise ValueError('Internship not found')

    deadline = intern['application_deadline']
    if deadline:
        try:
            d = datetime.strptime(deadline, '%Y-%m-%d').date()
            if d < date.today():
                conn.close()
                raise ValueError('Cannot apply: application deadline has passed')
        except Exception:
            # If parsing fails, ignore and allow application (but ideally input was validated when created)
            pass

    try:
        cur.execute("INSERT INTO applications (student_id, internship_id, note) VALUES (?, ?, ?)", (student_id, internship_id, note))
        conn.commit()
        last = cur.lastrowid
        return last
    except sqlite3.IntegrityError as e:
        raise ValueError('Application already exists or integrity error') from e
    finally:
        conn.close()


def get_applications_for_student(student_roll, db_path=DEFAULT_DB):
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id FROM students WHERE roll_no = ?", (student_roll.strip(),))
    row = cur.fetchone()
    if not row:
        conn.close()
        return []
    student_id = row['id']
    cur.execute("""
        SELECT a.id, i.title as internship_title, i.company, a.applied_at, a.status, a.note, i.id as internship_id
        FROM applications a
        JOIN internships i ON a.internship_id = i.id
        WHERE a.student_id = ?
        ORDER BY a.applied_at DESC
    """, (student_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_applications(db_path=DEFAULT_DB):
    pass

def change_application_status(application_id, new_status, db_path=DEFAULT_DB):
    pass
