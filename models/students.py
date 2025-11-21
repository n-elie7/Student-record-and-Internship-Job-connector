
class Student:
    """Student model for managing student records"""
    def __init__(self, db):
        self.db = db
        self.table_name = "students"

    def add_student(
        self,
        name: str,
        reg_no: str,
        age: int | None,
        course: str | None,
        gpa: float | None,
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

        return self.db._exec_table_insert(self.table_name, payload)

    def get_all_students(self):
        """Retrieve all students from the database."""
        return self.db._exec_table_select(self.table_name, "*")

    def find_student_by_reg_no(self, reg_no: str):
        """Find a student by their reg_no number."""
        res = self.db._exec_table_select(self.table_name, "*", {"reg_no": reg_no.strip()})
        return res[0] if res else None

    def search_students_by_name(self, name_substr: str):
        """function to search student by his/her name"""
        # use ilike filters via .ilike()
        res = (
            self.db.client.table(self.table_name).select("*").ilike("name", f"%{name_substr}%").execute()
        )
        return getattr(res, "data", None) or res.get("data", None)

    def update_student(self, reg_no: str, **fields):
        """Update student from database to new data"""
        allowed = {"name", "age", "course", "gpa"}
        payload = {k: v for k, v in fields.items() if k in allowed and v is not None}
        if not payload:
            raise ValueError("No valid fields to update.")
        # match by reg_no
        return self.db._exec_table_update(
            self.table_name, payload, {"reg_no": reg_no.strip()}
        )

    def delete_student(self, reg_no: str):
        """Delete a student from the database by their reg_no number."""
        return self.db._exec_table_delete(self.table_name, {"reg_no": reg_no.strip()})
