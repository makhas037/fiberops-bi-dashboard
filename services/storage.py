import os
import io
from dotenv import load_dotenv
from typing import Tuple, Optional

load_dotenv()


def upload_dataset_file(user_id: str, file_obj, filename: str, bucket: str = "datasets") -> Tuple[bool, dict]:
    """Upload a dataset file to Supabase storage using the service role key.

    Returns (success, payload). Payload contains metadata or error message.
    """
    try:
        from services.supabase_client import get_supabase_client
    except Exception:
        return False, {"error": "internal import error"}

    client = get_supabase_client(service=True)
    if not client:
        return False, {"error": "Supabase service client not configured"}

    try:
        file_obj.seek(0)
        data = file_obj.read()
        if isinstance(data, str):
            data = data.encode()
        key = f"{user_id}/{filename}"
        bio = io.BytesIO(data)
        bio.seek(0)
        client.storage.from_(bucket).upload(key, bio)
        meta = {"user_id": user_id, "file_name": filename, "storage_path": key, "file_size": len(data)}
        # try to infer simple metadata
        try:
            import pandas as pd
            bio.seek(0)
            if filename.lower().endswith(".csv"):
                df = pd.read_csv(bio)
            else:
                df = pd.read_excel(bio)
            meta["row_count"] = int(len(df))
            meta["column_names"] = list(df.columns)
        except Exception:
            pass
        return True, meta
    except Exception as e:
        return False, {"error": str(e)}


def download_dataset_bytes(storage_path: str, bucket: str = "datasets") -> Optional[bytes]:
    try:
        from services.supabase_client import get_supabase_client
    except Exception:
        return None
    client = get_supabase_client(service=True) or get_supabase_client()
    if not client:
        return None
    try:
        res = client.storage.from_(bucket).download(storage_path)
        # supabase-py may return bytes or a response-like; ensure bytes
        if isinstance(res, (bytes, bytearray)):
            return bytes(res)
        # some versions return a requests.Response-like object
        if hasattr(res, "content"):
            return res.content
        return None
    except Exception:
        return None


def get_public_url(storage_path: str, bucket: str = "datasets") -> Optional[str]:
    try:
        from services.supabase_client import get_supabase_client
    except Exception:
        return None
    client = get_supabase_client(service=True) or get_supabase_client()
    if not client:
        return None
    try:
        url = client.storage.from_(bucket).get_public_url(storage_path)
        # get_public_url may return dict-like
        if isinstance(url, dict):
            return url.get("publicUrl") or url.get("public_url")
        return url
    except Exception:
        return None
