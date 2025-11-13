from database import DEFAULT_DB, get_connection
from datetime import datetime


def add_internship(title, company=None, location=None, duration=None,
                   stipend=None, description=None, application_deadline=None,
                   db_path=DEFAULT_DB):
    conn = get_connection(db_path)
    
    cur = conn.cursor()

    if application_deadline:
        try:
            datetime.strftime(application_deadline, "%Y-%m-%d")
        except Exception as e:
            raise ValueError("Application deadline must be YYYY-MM-DD")

    try:
        cur.execute("INSERT INTO internships (title, company, location, duration, stipend, description, application_deadline) VALUES (?, ?, ?, ?, ?, ?, ?)", (title.strip(), company.strip(), location.strip(), duration.strip(), stipend.strip(), description.strip(), application_deadline.strip()))

        conn.commit()

        last_id = cur.lastrowid

        return last_id
    
    except Exception as e:
        raise ValueError("You entered wrong value") from e
    finally:
        conn.close()

def get_all_internships(db_path=DEFAULT_DB):
    try:
        conn = get_connection(db_path)
        cur = conn.cursor()

        cur.execute("SELECT * FROM internships ORDER BY application_deadline IS NULL, application_deadline ASC")

        rows= cur.fetchall()

        data = [dict(row) for row in rows]

        return data
    except Exception as e:
        raise ValueError("There is no data returned")
    finally:
        conn.close()

    

def get_open_internships(db_path=DEFAULT_DB):
    try:
        conn = get_connection(db_path)
        cur = conn.cursor()
        # Get today's date in YYYY-MM-DD format
        today = datetime.today().strftime("%Y-%m-%d")
        # Query to fetch internships with application deadlines in the future or no deadline
        cur.execute("SELECT * FROM internships WHERE application_deadline IS NULL OR application_deadline >= ? ORDER BY application_deadline IS NULL, application_deadline ASC", (today,))
        # Fetch all matching rows
        rows= cur.fetchall()
        # Convert rows to list of dictionaries
        data = [dict(row) for row in rows]
        # Return the list of open internships
        return data
    except Exception as e:
        # Raises an error if no data is returned
        raise ValueError("There is no data returned")
    finally:
        # Close the database connection
        conn.close()

def find_internship_by_id(internship_id, db_path=DEFAULT_DB):
    pass

def update_internship(internship_id, db_path=DEFAULT_DB, **fields):
    pass

def delete_internship(internship_id, db_path=DEFAULT_DB):
    
