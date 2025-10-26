import os
from dotenv import load_dotenv

load_dotenv()


def get_supabase_client(service: bool = False):
    """Return a configured supabase client or None if not configured.

    If service=True, prefer SUPABASE_SERVICE_KEY (server-side operations).
    """
    try:
        from supabase import create_client
    except Exception:
        return None

    url = os.getenv("SUPABASE_URL")
    if service:
        key = os.getenv("SUPABASE_SERVICE_KEY")
    else:
        key = os.getenv("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_SERVICE_KEY")
    if not url or not key:
        return None
    return create_client(url, key)
