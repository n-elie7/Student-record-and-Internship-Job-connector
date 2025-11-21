from datetime import datetime, date

class Application:
    """Application model for managing internship applications"""
    def __init__(self, db, student_model, internship_model):
        self.db = db
        self.student = student_model
        self.internship = internship_model
        self.table_name = "applications"

    def apply_to_internship(self, student_reg_no: str, internship_id: int, note: str | None):
        """Function to apply for internships"""
        student = self.student.find_student_by_reg_no(student_reg_no)
        if not student:
            raise ValueError("Student not found.")
        # Prevent applying after deadline: check internship
        intern = self.internship.find_internship_by_id(internship_id)
        if not intern:
            raise ValueError("Internship not found.")
        if intern.get("application_deadline"):
            # simple check

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
            return self.db._exec_table_insert(self.table_name, payload)
        except Exception as e:
            raise e

    def get_applications_for_student(self, student_reg_no: str):
        """function to get applications for specific students."""
        student = self.student.find_student_by_reg_no(student_reg_no)
        if not student:
            return []
        res = (
            self.db.client.table(self.table_name)
            .select(
                "id, internship_id, status, note, applied_at, internships(title,company)"
            )
            .eq("student_id", student["id"])
            .execute()
        )
        return getattr(res, "data", None) or res.get("data", None)

    def get_all_applications(self):
        """function to retrieve all applications"""
        res = (
            self.db.client.table(self.table_name)
            .select(
                "id, student_id, status, note, applied_at, students(name,reg_no), internships(title,company)"
            )
            .execute()
        )
        return getattr(res, "data", None) or res.get("data", None)

    def change_application_status(self, application_id: int, new_status: str):
        """Function to change application status"""
        allowed = {"Applied", "Shortlisted", "Rejected", "Hired", "Pending"}
        if new_status not in allowed:
            raise ValueError(f"Status must be one of {allowed}")
        return self.db._exec_table_update(
            self.table_name, {"status": new_status}, {"id": application_id}
        )
