from setup_env import SUPABASE_URL, SUPABASE_ANON_KEY
from supabase import create_client

class Database:
    """Database connection handler using Supabase"""
    def __init__(self):
        self.client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

    def _exec_table_select(self, table: str, cols="*", filters: dict | None = None):
        """Helper to execute a select query on a table with optional filters."""
        query = self.client.table(table).select(cols)

        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)

        res = query.execute()
        return res.data if hasattr(res, "data") else []

    def _exec_table_insert(self, table: str, payload: dict):
        """Helper to execute an insert query on a table."""
        res = self.client.table(table).insert(payload).execute()
        return res.data if hasattr(res, "data") else []

    def _exec_table_update(self, table: str, payload: dict, match: dict):
        """Helper to execute an update query on a table."""
        res = self.client.table(table).update(payload).match(match).execute()
        return res.data if hasattr(res, "data") else []

    def _exec_table_delete(self, table: str, match: dict):
        """Helper to execute a delete query on a table."""
        res = self.client.table(table).delete().match(match).execute()
        return res.data if hasattr(res, "data") else []
