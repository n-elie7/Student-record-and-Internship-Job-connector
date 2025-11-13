import os

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def get_supabase_client() -> Client:
    """Returns the Supabase client instance."""
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise RuntimeError("Please set SUPABASE_URL and SUPABASE_ANON_KEY environment variables.")
    return supabase

