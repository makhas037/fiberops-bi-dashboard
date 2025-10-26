import streamlit as st
import pandas as pd
import io
from services.database import DatabaseService
from services.storage import upload_dataset_file, download_dataset_bytes
from components.cards import render_dataset_card
from utils.validators import validate_file_size, validate_file_type


def render():
    st.header("💾 My Datasets")
    db: DatabaseService = st.session_state.get("db_service")
    user = st.session_state.get("user") or {"email": "dev"}
    user_id = (user.get("id") if isinstance(user, dict) else None) or user.get("email")

    uploaded = st.file_uploader("Upload dataset (CSV/XLSX/JSON)", type=["csv", "xlsx", "xls", "json"])
    if uploaded:
        st.write(f"File: {uploaded.name} ({uploaded.size} bytes)")
        ok_type, msg = validate_file_type(uploaded.name, [".csv", ".xlsx", ".xls", ".json"])
        ok_size, msg2 = validate_file_size(uploaded.size, max_mb=10)
        if not ok_type:
            st.error(msg)
        elif not ok_size:
            st.error(msg2)
        else:
            if st.button("Start Upload"):
                # perform server-side upload using service key when available
                success, payload = upload_dataset_file(user_id, uploaded, uploaded.name)
                if not success:
                    st.error(f"Upload failed: {payload.get('error')}")
                else:
                    # store metadata in DB if possible
                    if db and db.client:
                        try:
                            meta = payload.copy()
                            meta.update({"user_id": user_id})
                            db.client.table("datasets").insert(meta).execute()
                        except Exception:
                            pass
                    st.success("Uploaded successfully")

    st.markdown("---")
    st.subheader("Your datasets")
    if not db or not db.client:
        st.info("No database client configured; datasets list unavailable.")
        return
    datasets = db.get_user_datasets(user_id)
    if not datasets:
        st.info("No datasets found")
        return

    for ds in datasets:
        def _apply(d):
            st.session_state["active_dataset"] = d
            st.success(f"Applied dataset: {d.get('file_name')}")

        def _preview(d):
            storage_path = d.get("storage_path")
            b = download_dataset_bytes(storage_path)
            if not b:
                st.error("Unable to download dataset preview")
                return
            try:
                df = pd.read_csv(io.BytesIO(b))
            except Exception:
                try:
                    df = pd.read_excel(io.BytesIO(b))
                except Exception:
                    st.error("Unable to parse dataset preview")
                    return
            st.dataframe(df.head(40))

        def _delete(d):
            # simple delete: remove DB record (and optionally storage object)
            if db and db.client:
                try:
                    db.client.table("datasets").delete().eq("storage_path", d.get("storage_path")).execute()
                    st.success("Dataset record removed (storage object may remain)")
                except Exception as e:
                    st.error(f"Delete failed: {e}")

        render_dataset_card(ds, on_apply=_apply, on_view=_preview, on_delete=_delete)
