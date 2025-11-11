import sqlite3
from database import DEFAULT_DB


def apply_to_internship(student_roll, internship_id, note=None, db_path=DEFAULT_DB):
    conn = get_connection(db_path)
    cur = conn.cursor()
    try:
        # Get student ID from roll number
        cur.execute("SELECT id FROM students WHERE roll_no = ?", (student_roll.strip(),))
        student = cur.fetchone()
        if not student:
            raise ValueError("Student with the given roll number does not exist.")
        student_id = student["id"]

        # Check if internship exists
        cur.execute("SELECT id FROM internships WHERE id = ?", (internship_id,))
        internship = cur.fetchone()
        if not internship:
            raise ValueError("Internship with the given ID does not exist.")

        # Insert application record
        cur.execute("INSERT INTO applications (student_id, internship_id, note) VALUES (?, ?, ?)",
                    (student_id, internship_id, note.strip() if note else None))
        conn.commit()

        application_id = cur.lastrowid
        return application_id

    except sqlite3.IntegrityError:
        raise ValueError("The student has already applied to this internship.")
    except Exception as e:
        raise ValueError("Failed to apply to internship.") from e
    finally:
        conn.close()

def get_applications_for_student(student_roll, db_path=DEFAULT_DB):
    pass

def get_all_applications(db_path=DEFAULT_DB):
    pass

def change_application_status(application_id, new_status, db_path=DEFAULT_DB):
    pass
