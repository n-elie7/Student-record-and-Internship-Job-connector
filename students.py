from helper_wrappers import (
    _exec_table_delete,
    _exec_table_insert,
    _exec_table_select,
    _exec_table_update,
)
from setup_env import supabase as sb


def add_student(
    name: str, reg_no: str, age: int | None, course: str | None, gpa: float | None
):
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


def find_student_by_reg_no(reg_no: str):
    """Find a student by their roll number."""
    res = _exec_table_select("students", "*", {"reg_no": reg_no.strip()})
    return res[0] if res else None


def search_students_by_name(name_substr: str):
    # use ilike filters via .ilike()
    res = sb.table("students").select("*").ilike("name", f"%{name_substr}%").execute()
    return getattr(res, "data", None) or res.get("data", None)


def update_student(reg_no: str, **fields):
    allowed = {"name", "age", "course", "gpa"}
    payload = {k: v for k, v in fields.items() if k in allowed and v is not None}
    if not payload:
        raise ValueError("No valid fields to update.")
    # match by reg_no
    return _exec_table_update("students", payload, {"reg_no": reg_no.strip()})


def delete_student(reg_no: str):
    """Delete a student from the database by their roll number."""
    return _exec_table_delete("students", {"reg_no": reg_no.strip()})
