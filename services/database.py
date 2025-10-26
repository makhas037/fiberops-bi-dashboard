import os
import io
from uuid import uuid4
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
import os
import io
from uuid import uuid4
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


class DatabaseService:
    """Lightweight wrapper around Supabase client for common operations."""

    def __init__(self, supabase_client=None):
        try:
            from supabase import create_client
        except Exception as e:
            # allow import error to be handled at runtime
            self.client = None
            return

        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_ANON_KEY")
        if not url or not key:
            # Allow running without Supabase in dev, but operations will return safe defaults
            self.client = None
            return

        self.client = supabase_client or create_client(url, key)

    def add_dataset(self, user_id: str, file_obj, filename: str, bucket: str = "datasets"):
        if not self.client:
            return {"success": False, "error": "Supabase client not configured"}
        try:
            file_obj.seek(0)
            data = file_obj.read()
            if isinstance(data, str):
                data = data.encode()
            key = f"{user_id}/{uuid4().hex}_{filename}"
            bio = io.BytesIO(data)
            bio.seek(0)
            # Upload using storage API
            self.client.storage.from_(bucket).upload(key, bio)
            meta = {
                "user_id": user_id,
                "file_name": filename,
                "storage_path": key,
                "file_size": len(data),
            }
            try:
                bio.seek(0)
                if filename.lower().endswith(".csv"):
                    df = pd.read_csv(bio)
                else:
                    df = pd.read_excel(bio)
                meta["row_count"] = int(len(df))
                meta["column_names"] = list(df.columns)
            except Exception:
                pass
            res = self.client.table("datasets").insert(meta).execute()
            return {"success": True, "meta": meta, "insert": getattr(res, "data", res)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_user_datasets(self, user_id: str):
        if not self.client:
            return []
        try:
            res = self.client.table("datasets").select("*").eq("user_id", user_id).order("created_at", {"ascending": False}).execute()
            return getattr(res, "data", res) or []
        except Exception:
            return []

    def get_user_profile(self, user_id: str):
        if not self.client:
            return {}
        try:
            table = "user_profiles" if self._table_exists("user_profiles") else "profiles"
            res = self.client.table(table).select("*").eq("user_id", user_id).single().execute()
            return getattr(res, "data", res) or {}
        except Exception:
            return {}

    def _table_exists(self, table_name: str) -> bool:
        if not self.client:
            return False
        try:
            _ = self.client.table(table_name).select("id").limit(1).execute()
            return True
        except Exception:
            return False
