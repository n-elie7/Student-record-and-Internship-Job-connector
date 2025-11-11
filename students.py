import sqlite3
from database import DEFAULT_DB, get_connection

def add_student(name, reg_no, age=None, course=None, gpa=None, db_path=DEFAULT_DB):

    conn = get_connection(db_path)
    #Get connection to the SQL database
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO students (name, reg_no, age, course, gpa) VALUES (?, ?, ?, ?, ?)",
            (name.strip(), reg_no.strip(), age.strip(), course.strip(), gpa.strip())
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
    # connect the function to the SQL datatbase.
    conn = get_connection(db_path)
    # create a cursor object to execute SQL commands
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM students WHERE roll_no=?", (roll_no.strip(), ))
        student = cur.fetchone()
        if student is None:
            raise ValueError("ROLL NUMBER NOT FOUND")
        return dict(student)
    finally:
        conn.close()
def search_students_by_name(name_substr, db_path=DEFAULT_DB):
    pass

def update_student(roll_no, db_path=DEFAULT_DB, **fields):
    pass

def delete_student(reg_no, dp_path=DEFAULT_DB):
    #Get the function to connect with the SQL database
    conn = get_connection(dp_path)
    cur = conn.cursor()
    #We can delete student using the reg_no
    try:
        cur.execute("DELETE FROM students WHERE roll_no=?", (reg_no.strip(), ))
        conn.commit()
        #The changes to be saved in database
        affected = cur.rowcount
        # counts the number of rows that have been modified by last SQL command. 
        return affected
    except ValueError:
        print("REGISTRATION NUMBER NOT FOUND")
    finally:
        # close the connection
        conn.close()
        
    