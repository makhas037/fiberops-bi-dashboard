import streamlit as st


def render_breadcrumbs(items: list[str]):
    st.write(" > ".join(items))


def render_tabs(tabs: list[str], active: int = 0):
    cols = st.columns(len(tabs))
    for i, t in enumerate(tabs):
        with cols[i]:
            if st.button(t):
                st.session_state['active_tab'] = i
    return st.session_state.get('active_tab', active)
