import streamlit as st


def show_delete_confirmation(item_name: str) -> bool:
    st.warning(f"Are you sure you want to delete {item_name}? This action cannot be undone.")
    cols = st.columns(2)
    if cols[1].button("Delete"):
        return True
    if cols[0].button("Cancel"):
        return False
    return False


def show_dataset_preview(dataset: dict):
    st.subheader(dataset.get("file_name"))
    df = dataset.get("preview_df")
    if df is not None:
        st.dataframe(df.head(20))
    else:
        st.info("No preview available")
