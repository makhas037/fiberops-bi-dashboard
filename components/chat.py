import streamlit as st


def render_chat_ui():
    st.header("Fick AI")
    if "fick_history" not in st.session_state:
        st.session_state.fick_history = []
    prompt = st.chat_input("Ask Fick something...")
    if prompt:
        st.session_state.fick_history.append({"user": prompt})
        st.experimental_rerun()
    for msg in st.session_state.fick_history:
        if 'user' in msg:
            st.chat_message("user").write(msg['user'])
        else:
            st.chat_message("assistant").write(msg.get('assistant', ''))
