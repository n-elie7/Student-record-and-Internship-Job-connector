from setup_env import supabase as sb


def _exec_table_select(table: str, cols="*"):
    """Helper to execute a select query on a table with optional filters."""
    query = sb.table(table).select(cols)

    res = query.execute()
    return res.data if hasattr(res, 'data') else []

def _exec_table_insert(table: str, payload: dict):
    """Helper to execute an insert query on a table."""
    res = sb.table(table).insert(payload).execute()
    return res.data if hasattr(res, 'data') else []

def _exec_table_update(table: str, payload: dict, match: dict):
    """Helper to execute an update query on a table."""
    res = sb.table(table).update(payload).match(match).execute()
    return res.data if hasattr(res, 'data') else []

def _exec_table_delete(table: str, match: dict):
    """Helper to execute a delete query on a table."""
    res = sb.table(table).delete().match(match).execute()
    return res.data if hasattr(res, 'data') else []
