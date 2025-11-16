from helper_wrappers import _exec_table_insert, _exec_table_update
from internships import find_internship_by_id
from students import find_student_by_reg_no
from setup_env import supabase as sb


def apply_to_internship(student_roll: str, internship_id: int, note: str | None):
    student = find_student_by_reg_no(student_roll)
    if not student:
        raise ValueError("Student not found.")
    # Prevent applying after deadline: check internship
    intern = find_internship_by_id(internship_id)
    if not intern:
        raise ValueError("Internship not found.")
    if intern.get("application_deadline"):
        # simple check
        from datetime import datetime, date

        try:
            d = datetime.strptime(intern["application_deadline"], "%Y-%m-%d").date()
            if d < date.today():
                raise ValueError("Cannot apply: application deadline has passed.")
        except ValueError:
            # If date parse fails, ignore
            pass
    payload = {"student_id": student["id"], "internship_id": internship_id}
    if note:
        payload["note"] = note
    try:
        return _exec_table_insert("applications", payload)
    except Exception as e:
        raise e


def get_applications_for_student(student_roll: str):
    student = find_student_by_reg_no(student_roll)
    if not student:
        return []
    res = (
        sb.table("applications")
        .select(
            "id, internship_id, status, note, applied_at, internships(title,company)"
        )
        .eq("student_id", student["id"])
        .execute()
    )
    return getattr(res, "data", None) or res.get("data", None)


def get_all_applications():
    res = (
        sb.table("applications")
        .select(
            "id, student_id, status, note, applied_at, students(name,roll_no), internships(title,company)"
        )
        .execute()
    )
    return getattr(res, "data", None) or res.get("data", None)


def change_application_status(application_id: int, new_status: str):
    allowed = {"Applied", "Shortlisted", "Rejected", "Hired", "Pending"}
    if new_status not in allowed:
        raise ValueError(f"Status must be one of {allowed}")
    return _exec_table_update(
        "applications", {"status": new_status}, {"id": application_id}
    )
