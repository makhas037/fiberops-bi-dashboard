import streamlit as st

def render():
    st.header("❓ Help Center")
    st.write("Search docs or contact support.")
    q = st.text_input("Search help articles")
    if q:
        st.info("No docs indexed yet. This is a placeholder.")
