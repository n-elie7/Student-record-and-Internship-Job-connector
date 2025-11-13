from helper_wrappers import _exec_table_insert


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
