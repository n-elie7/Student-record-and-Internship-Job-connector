from helper_wrappers import _exec_table_insert, _exec_table_select
from setup_env import supabase as sb


def add_student(name: str, reg_no: str, age: int | None, course: str | None, gpa: float | None):
    """Add a new student to the database."""
    payload = {"name": name.strip(), "reg_no": reg_no.strip()}
    # Check for optional fields
    if age is not None: 
        payload["age"] = age
    if course: 
        payload["course"] = course
    if gpa is not None: 
        payload["gpa"] = float(gpa)

    return _exec_table_insert("students", payload)

def get_all_students():
    """Retrieve all students from the database."""
    return _exec_table_select("students", "*")

def find_student_by_roll(roll_no: str):
    """Find a student by their roll number."""
    res = _exec_table_select("students", "*", {"roll_no": roll_no.strip()})
    return res[0] if res else None

def search_students_by_name(name_substr: str):
    # use ilike filters via .ilike()
    res = sb.table("students").select("*").ilike("name", f"%{name_substr}%").execute()
    return getattr(res, "data", None) or res.get("data", None)
