import sqlite3
from database import DEFAULT_DB, get_connection

def validate_student_data(name, roll_no, age, course, gpa):
 """Check if the student data is valid."""
 if not name or not roll_no:
        raise ValueError("Name and Roll Number cannot be empty.")
 if age is not None:
        try:
            age =int(age)
            if age <= 0:
                raise ValueError("Age must be positive.")
        except ValueError:
            raise ValueError("Age must be a valid number.")
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
    # Get connection to our database
    conn = get_connection(db_path)
    # create cursor
    cur = conn.cursor()

    try:
        # Querying to fetch all students from database
        cur.execute("SELECT * FROM students ORDER BY name")

        rows = cur.fetchall()
        data = [dict(row) for row in rows]

        return data
    except:
        raise ValueError("Failed to get all students")
    finally:
        conn.close()

def find_student_by_roll(reg_no, db_path=DEFAULT_DB):
    # get connection to the database
    conn = get_connection(db_path)
    # create cursor
    cur = conn.cursor()

    try: 
        # finding student by roll
        cur.execute("SELECT * FROM students WHERE roll_no = ?", (reg_no.strip(),))
   
        row = cur.fetchone()
        data = dict(row) if row else None 

        return data
    except:
        raise ValueError("Failed to get student")
    finally:
        conn.close()
    
        



def search_students_by_name(name, db_path=DEFAULT_DB):
    #get connection to our database
    conn = get_connection(db_path)
    # ceate cursor
    cur = conn.cursor()

    try:
        # finding student by name
        cur.execute("SELECT * FROM students WHERE name = ?", (name.strip(),))

        row = cur.fetchone()
        data = dict(row) if row else None

        return data
    except:
        raise ValueError("Failed to get student")
    finally:
        conn.close()
        


def update_student(roll_no, db_path=DEFAULT_DB, **fields):
    # get connection to our database
    conn = get_connection(db_path)
    # create cursor
    cur = conn.cursor()
    # We can update student using the roll_no
    try:
        #to set the clause for updating fields dynamically
        set_clause = ", ".join([f"{key} = ?" for key in fields.keys()])
        values = list(fields.values())
        values.append(roll_no.strip())  
        #the SQL query to update student details
        sql = f"UPDATE students SET {set_clause} WHERE roll_no = ?"
        cur.execute(sql, values)
        #
        conn.commit()
        affected = cur.rowcount  
        
        return affected
    except Exception as e:
        raise ValueError("Failed to update student") from e
    finally:
        conn.close()

def delete_student(reg_no, dp_path=DEFAULT_DB):
    #Get the function to connect with the SQL database
    conn = get_connection(dp_path)
    # create cursor
    cur = conn.cursor()
    # We can delete student using the reg_no
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
        
    