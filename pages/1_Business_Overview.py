import streamlit as st
import pandas as pd
import plotly.express as px

import streamlit as st
import pandas as pd
from components.cards import render_kpi_card
from components.charts import render_line_chart, render_pie_chart
from services.database import DatabaseService
from services.storage import download_dataset_bytes
import io


def render():
    st.header("📈 Analytics Dashboard")

    # Ensure session and services are available
    db: DatabaseService = st.session_state.get("db_service")
    user = st.session_state.get("user") or {"email": "dev"}
    user_id = (user.get("id") if isinstance(user, dict) else None) or user.get("email")

    # Dataset selector: prefer active dataset in session
    datasets = []
    if db:
        datasets = db.get_user_datasets(user_id)

    options = [d.get("file_name") for d in datasets] if datasets else []
    selected = st.selectbox("Select dataset", ["(sample)"] + options, index=0)

    if selected == "(sample)":
        # try local sample
        try:
            df = pd.read_csv("data/sample_data/demo_sales_data.csv")
        except Exception:
            df = pd.DataFrame({
                "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                "revenue": [12000, 15000, 18000, 22000, 26000, 30000],
                "category": ["Electronics", "Clothing", "Food", "Home", "Electronics", "Food"],
            })
    else:
        ds = next((d for d in datasets if d.get("file_name") == selected), None)
        df = None
        if ds:
            storage_path = ds.get("storage_path")
            b = download_dataset_bytes(storage_path)
            if b:
                try:
                    df = pd.read_csv(io.BytesIO(b))
                except Exception:
                    try:
                        df = pd.read_excel(io.BytesIO(b))
                    except Exception:
                        st.error("Unable to parse selected dataset")
        if df is None:
            st.info("Selected dataset could not be loaded; showing sample instead.")
            try:
                df = pd.read_csv("data/sample_data/demo_sales_data.csv")
            except Exception:
                df = pd.DataFrame({
                    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                    "revenue": [12000, 15000, 18000, 22000, 26000, 30000],
                    "category": ["Electronics", "Clothing", "Food", "Home", "Electronics", "Food"],
                })

    # compute simple KPIs
    total_revenue = df.get("revenue").sum() if "revenue" in df.columns else df.shape[0]
    avg_value = int(df.get("revenue").mean()) if "revenue" in df.columns else "-"
    unique_cats = df["category"].nunique() if "category" in df.columns else "-"
    months = df["month"].nunique() if "month" in df.columns else df.shape[0]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card("Total Revenue", f"${total_revenue:,}")
    with c2:
        render_kpi_card("Average Value", f"${avg_value}")
    with c3:
        render_kpi_card("Unique Categories", f"{unique_cats}")
    with c4:
        render_kpi_card("Periods", f"{months}")

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if "month" in df.columns and "revenue" in df.columns:
            render_line_chart(df, "month", "revenue", title="📈 Revenue Over Time")
    with c2:
        if "category" in df.columns:
            pie = df["category"].value_counts().reset_index()
            pie.columns = ["category", "count"]
            render_pie_chart(pie, names="category", values="count", title="🎯 Category Breakdown")
