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

def delete_student(reg_no, dp_path=DEFAULT_DB):
    #Get the function to connect with the SQL database
    conn = get_connection(dp_path)
    cur = conn.cursor()
    #We can delete student using the roll_no 
    try:
        cur.execute("DELETE FROM students WHERE roll_no=?", (reg_no.strip(), ))
        conn.commit()
        #The changes to be saved in database
        if cur.rowcount != 0:
            #counts the number of rows that have been modified by last SQL command. 
            print("THE STUDENT HAS BEEN DELETED SUCCESSFULLY.")
    except ValueError:
        print("REGISTRATION NUMBER NOT FOUND")
    finally:
        conn.close()
        #closes the database
    