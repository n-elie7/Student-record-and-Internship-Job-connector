from datetime import datetime
import time


class Internship:
    """Internship model for managing internship opportunities"""
    def __init__(self, db):
        self.db = db
        self.table_name = "internships"

    def add_internship(
        self,
        title: str,
        company: str | None,
        location: str | None,
        duration: str | None,
        stipend: str | None,
        description: str | None,
        application_deadline: str | None,
    ):
        """Adds a new internship to the database."""
        payload = {"title": title.strip()}
        if company:
            payload["company"] = company
        if location:
            payload["location"] = location
        if duration:
            payload["duration"] = duration
        if stipend:
            payload["stipend"] = stipend
        if description:
            payload["description"] = description
        if application_deadline:
            datetime.strftime(application_deadline, "%Y-%m-%d")
            payload["application_deadline"] = application_deadline

        return self.db._exec_table_insert(self.table_name, payload)

    def get_all_internships(self):
        """Retrieves all internships from the database."""
        return self.db._exec_table_select(self.table_name, "*")

    def get_open_internships(self):
        """Retrieves all internships with application deadlines in the future or null."""
        today = time.strftime("%Y-%m-%d")
        # include null deadlines as open too
        res = (
            self.db.client.table(self.table_name)
            .select("*")
            .or_(f"application_deadline.is.null,application_deadline.gte.{today}")
            .execute()
        )
        return getattr(res, "data", None) or res.get("data", None)

    def find_internship_by_id(self, intern_id: int):
        """Finds an internship by its ID."""
        res = self.db._exec_table_select(self.table_name, "*", {"id": intern_id})
        return res[0] if res else None

    def update_internship(self, internship_id: int, **fields):
        """Updates an existing internship with the provided fields."""
        allowed = {
            "title",
            "company",
            "location",
            "duration",
            "stipend",
            "description",
            "application_deadline",
        }
        payload = {k: v for k, v in fields.items() if k in allowed and v is not None}
        if not payload:
            raise ValueError("No valid fields to update")
        return self.db._exec_table_update(self.table_name, payload, {"id": internship_id})

    def delete_internship(self, internship_id: int):
        """Deletes an internship by its ID."""
        return self.db._exec_table_delete(self.table_name, {"id": internship_id})
