import streamlit as st
from typing import Optional


def render_kpi_card(title: str, value: str, delta: Optional[str] = None, key: Optional[str] = None):
    col = st.container()
    with col:
        st.markdown(f"<div class='metric-card' id='{key or title}' style='padding:12px;border-radius:10px;background:var(--card-background, #0f172a);'>"
                    f"<div style='font-size:12px;color:var(--text-secondary,#94A3B8);'>{title}</div>"
                    f"<div style='font-size:22px;font-weight:700;margin-top:6px;color:var(--text-primary,#F8FAFC);'>{value}</div>"
                    f"<div style='font-size:12px;margin-top:6px;color:var(--text-secondary,#94A3B8);'>{delta or ''}</div>"
                    f"</div>", unsafe_allow_html=True)


def render_dataset_card(dataset: dict, on_apply=None, on_view=None, on_delete=None):
    name = dataset.get("file_name")
    rows = dataset.get("row_count") or "-"
    size = dataset.get("file_size") or 0
    cols = len(dataset.get("column_names") or [])
    st.markdown(f"**{name}**")
    st.text(f"{rows} rows · {cols} columns · {int(size)/1024:.2f} KB")
    c1, c2, c3 = st.columns([1,1,1])
    if c1.button("Apply", key=f"apply_{name}") and on_apply:
        on_apply(dataset)
    if c2.button("Preview", key=f"preview_{name}") and on_view:
        on_view(dataset)
    if c3.button("Delete", key=f"delete_{name}") and on_delete:
        on_delete(dataset)
