from datetime import datetime
import time
from helper_wrappers import (
    _exec_table_delete,
    _exec_table_insert,
    _exec_table_select,
    _exec_table_update,
)
from setup_env import supabase as sb


def add_internship(
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

    return _exec_table_insert("internships", payload)


def get_all_internships():
    """Retrieves all internships from the database."""
    return _exec_table_select("internships", "*")


def get_open_internships():
    """Retrieves all internships with application deadlines in the future or null."""
    today = time.strftime("%Y-%m-%d")
    # include null deadlines as open too
    res = (
        sb.table("internships")
        .select("*")
        .or_(f"application_deadline.is.null,application_deadline.gte.{today}")
        .execute()
    )
    return getattr(res, "data", None) or res.get("data", None)


def find_internship_by_id(intern_id: int):
    """Finds an internship by its ID."""
    res = _exec_table_select("internships", "*", {"id": intern_id})
    return res[0] if res else None


def update_internship(internship_id: int, **fields):
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
    return _exec_table_update("internships", payload, {"id": internship_id})


def delete_internship(internship_id: int):
    """Deletes an internship by its ID."""
    return _exec_table_delete("internships", {"id": internship_id})
