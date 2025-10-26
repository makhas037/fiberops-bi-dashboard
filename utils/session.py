import streamlit as st
from typing import Any
from datetime import datetime, timedelta


def initialize_session_state():
    """Initialize session state with default values used across the app.

    This is safe to call multiple times.
    """
    defaults = {
        "user": None,
        "authenticated": False,
        "auth_token": None,
        "remember_me": False,
        "current_workspace": None,
        "active_dataset": None,
        "dark_mode": True,
        "sidebar_collapsed": False,
        "nav": "🏢 Business Overview",
        "notification_count": 0,
        "last_activity": datetime.utcnow(),
        "session_timeout_minutes": 60,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def get_session_value(key: str, default: Any = None) -> Any:
    return st.session_state.get(key, default)


def set_session_value(key: str, value: Any):
    st.session_state[key] = value
    if key != "last_activity":
        st.session_state["last_activity"] = datetime.utcnow()


def clear_session():
    keys = list(st.session_state.keys())
    for k in keys:
        del st.session_state[k]
    # re-initialize a fresh set of defaults
    initialize_session_state()


def check_session_timeout() -> bool:
    """Return True if session still valid, otherwise clear and return False."""
    last = st.session_state.get("last_activity")
    timeout_min = st.session_state.get("session_timeout_minutes", 60)
    if not last:
        return True
    if isinstance(last, str):
        try:
            last = datetime.fromisoformat(last)
        except Exception:
            last = datetime.utcnow()
    if datetime.utcnow() - last > timedelta(minutes=timeout_min):
        # timeout
        clear_session()
        return False
    # keep alive
    st.session_state["last_activity"] = datetime.utcnow()
    return True


# Backwards-compatible alias used by earlier code
def init_session_state():
    """Deprecated alias for initialize_session_state; kept for backwards compatibility."""
    return initialize_session_state()
