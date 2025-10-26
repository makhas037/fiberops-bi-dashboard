import streamlit as st
from utils.validators import validate_email, validate_password
from utils.auth import login_user, signup_user


def render_login_form():
    st.subheader("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    remember = st.checkbox("Remember me", key="login_remember")
    if st.button("Login"):
        ok, msg = login_user(email, password, remember_me=remember)
        if ok:
            st.success("Login successful")
            st.experimental_rerun()
        else:
            st.error(f"Login failed: {msg}")


def render_signup_form():
    st.subheader("Create an account")
    name = st.text_input("Full name", key="signup_name")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    password2 = st.text_input("Confirm password", type="password", key="signup_password2")
    if st.button("Create account"):
        valid, err = validate_email(email)
        if not valid:
            st.error(err)
            return
        vp, perr = validate_password(password)
        if not vp:
            st.error(perr)
            return
        if password != password2:
            st.error("Passwords do not match")
            return
        ok, msg = signup_user(email, password, full_name=name)
        if ok:
            import streamlit as st
            from utils.validators import validate_email, validate_password
            from utils.auth import login_user, signup_user


            def render_login_form():
                st.subheader("Login")
                email = st.text_input("Email", key="login_email")
                password = st.text_input("Password", type="password", key="login_password")
                remember = st.checkbox("Remember me", key="login_remember")
                if st.button("Login"):
                    ok, msg = login_user(email, password, remember_me=remember)
                    if ok:
                        st.success("Login successful")
                        st.experimental_rerun()
                    else:
                        st.error(f"Login failed: {msg}")


            def render_signup_form():
                st.subheader("Create an account")
                name = st.text_input("Full name", key="signup_name")
                email = st.text_input("Email", key="signup_email")
                password = st.text_input("Password", type="password", key="signup_password")
                password2 = st.text_input("Confirm password", type="password", key="signup_password2")
                if st.button("Create account"):
                    valid, err = validate_email(email)
                    if not valid:
                        st.error(err)
                        return
                    vp, perr = validate_password(password)
                    if not vp:
                        st.error(perr)
                        return
                    if password != password2:
                        st.error("Passwords do not match")
                        return
                    ok, msg = signup_user(email, password, full_name=name)
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)
