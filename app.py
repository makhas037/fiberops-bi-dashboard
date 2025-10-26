import streamlit as st
from utils.session import initialize_session_state
from utils.auth import check_authentication
from components.layout_v2 import render_sidebar, render_header
from services.database import DatabaseService
import importlib


def main():
    initialize_session_state()

    if "db_service" not in st.session_state:
        try:
            st.session_state["db_service"] = DatabaseService()
        except Exception as e:
            st.session_state["db_service"] = None
            st.warning(f"Database service init warning: {e}")

    # If not authenticated, show login/signup forms (handled by components/forms)
    if not check_authentication():
        from components.forms import render_login_form, render_signup_form
        st.markdown("# Welcome to FiberOps")
        cols = st.columns(2)
        with cols[0]:
            render_login_form()
        with cols[1]:
            render_signup_form()
        return

    # Authenticated UI
    render_sidebar()
    render_header()

    page = st.session_state.get("nav", "🏢 Business Overview")
    page_key = {
        "🏢 Business Overview": "pages.1_Business_Overview",
        "💾 Datasets": "pages.4_Datasets",
        "⚙️ Settings": "pages.6_Settings",
        "✨ Fick AI": "pages.3_Fick_AI",
        "📊 Analytics": "pages.2_Analytics",
        "💼 Workspaces": "pages.5_Workspaces",
        "❓ Help": "pages.7_Help_Center",
    }

    module_name = page_key.get(page)
    if module_name:
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, "render"):
                module.render()
            else:
                st.info(f"Page module '{module_name}' has no render() function yet.")
        except ModuleNotFoundError:
            st.info(f"Page '{page}' not implemented yet.")
        except Exception as e:
            st.error(f"Error loading page '{page}': {e}")
    else:
        st.info("No page selected")


if __name__ == "__main__":
    main()
