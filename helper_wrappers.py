from setup_env import supabase as sb


def _exec_table_select(table: str, cols="*"):
    """Helper to execute a select query on a table with optional filters."""
    query = sb.table(table).select(cols)

    res = query.execute()
    return getattr(res, "data", None) or res.get("data", None)

def _exec_table_insert(table: str, payload: dict):
    """Helper to execute an insert query on a table."""
    res = sb.table(table).insert(payload).execute()
    return getattr(res, "data", None) or res.get("data", None)

