import streamlit as st
from services.database import DatabaseService

def render():
    st.header("⚙️ Settings")
    db: DatabaseService = st.session_state.get('db_service')
    user = st.session_state.get('user') or {'email':'dev'}
    user_id = user.get('id') or user.get('email')

    tabs = st.tabs(["Profile","Notifications","Security","Appearance","Billing"])
    with tabs[0]:
        st.subheader("Profile")
        profile = db.get_user_profile(user_id) if db else {}
        name = st.text_input("Full name", value=profile.get('full_name','Alex Jerome'))
        email = st.text_input("Email", value=profile.get('email',user.get('email')))
        if st.button("Save profile"):
            if not db:
                st.error("DB not configured")
            else:
                res = db.client.table('user_profiles').upsert({'user_id': user_id, 'full_name': name, 'email': email}).execute()
                st.success("Saved")
