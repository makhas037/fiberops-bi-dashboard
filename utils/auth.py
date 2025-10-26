import os
from typing import Optional, Tuple
import streamlit as st
from datetime import datetime

from services.database import DatabaseService
from services.supabase_client import get_supabase_client
from utils.session import initialize_session_state, set_session_value, get_session_value, clear_session


def login_user(email: str, password: str, remember_me: bool = False) -> Tuple[bool, str]:
    """Authenticate a user via Supabase Auth. Stores user in session_state on success.

    Returns (success, message).
    """
    initialize_session_state()
    client = get_supabase_client()
    if not client:
        return False, "Supabase client not configured. Set SUPABASE_URL and keys in environment."
    try:
        res = client.auth.sign_in_with_password({"email": email, "password": password})
        # supabase-py returns a dict-like response; normalize
        data = res.get("data") or res
        if res.get("error"):
            err = res.get("error")
            msg = err.get("message") if isinstance(err, dict) else str(err)
            return False, msg

        user = data.get("user") if isinstance(data, dict) else data
        session_info = data.get("session", {}) if isinstance(data, dict) else {}
        token = session_info.get("access_token")
        refresh_token = session_info.get("refresh_token")

        # store session
        set_session_value("user", user or {"email": email})
        set_session_value("authenticated", True)
        set_session_value("auth_token", token)
        set_session_value("remember_me", bool(remember_me))

        # fetch profile if available
        try:
            db = DatabaseService(get_supabase_client())
            uid = (user.get("id") if user else None) or email
            profile = db.get_user_profile(uid)
            set_session_value("user_profile", profile or {})
        except Exception:
            set_session_value("user_profile", {})

        # NOTE: persistent "remember me" tokens to disk were removed for security.
        # For production, implement secure server-side sessions or encrypted cookies.

        return True, "Logged in"
    except Exception as e:
        return False, str(e)


# Removed on-disk persistence helpers for security reasons.


def signup_user(email: str, password: str, full_name: Optional[str] = None) -> Tuple[bool, str]:
    client = get_supabase_client()
    if not client:
        return False, "Supabase client not configured"
    try:
        # newer supabase-py supports options
        res = client.auth.sign_up({"email": email, "password": password, "options": {"data": {"full_name": full_name}}})
        if res.get("error"):
            err = res.get("error")
            return False, err.get("message") if isinstance(err, dict) else str(err)
        # create profile row via DatabaseService if available
        try:
            db = DatabaseService(get_supabase_client())
            user = res.get("data", {}).get("user") or res.get("user")
            uid = (user.get("id") if isinstance(user, dict) else None) or email
            db.client.table("user_profiles").insert({"user_id": uid, "full_name": full_name, "email": email}).execute()
        except Exception:
            pass
        return True, "Signup initiated; check your email to confirm"
    except Exception as e:
        return False, str(e)


def logout_user():
    """Sign out locally and from Supabase if possible."""
    client = get_supabase_client()
    try:
        if client:
            client.auth.sign_out()
    except Exception:
        pass
    clear_session()


def check_authentication() -> bool:
    """Return True if authenticated and session valid. Performs timeout check."""
    initialize_session_state()
    if not get_session_value("authenticated"):
        # No persistent remember-me is available; require fresh login.
        return False
    # check timeout
    from utils.session import check_session_timeout

    return check_session_timeout()


def get_current_user():
    initialize_session_state()
    return get_session_value("user")


def reset_password(email: str) -> Tuple[bool, str]:
    client = get_supabase_client()
    if not client:
        return False, "Supabase client not configured"
    try:
        client.auth.reset_password_for_email(email)
        return True, "Password reset email sent"
    except Exception as e:
        return False, str(e)
