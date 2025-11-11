from database import DEFAULT_DB


def add_internship(title, company=None, location=None, duration=None,
                   stipend=None, description=None, application_deadline=None,
                   db_path=DEFAULT_DB):
    pass

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
