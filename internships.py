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
    pass

def get_open_internships(db_path=DEFAULT_DB):
    pass

def find_internship_by_id(internship_id, db_path=DEFAULT_DB):
    pass

def update_internship(internship_id, db_path=DEFAULT_DB, **fields):
    pass

def delete_internship(internship_id, db_path=DEFAULT_DB):
    pass
