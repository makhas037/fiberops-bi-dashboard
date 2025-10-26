import streamlit as st

def render_sidebar():
    """Render the main navigation sidebar"""
    with st.sidebar:
        # logo placeholder
        try:
            st.image("assets/images/logo.png", width=140)
        except Exception:
            st.markdown("<div style='font-weight:700; font-size:20px'>📊 FiberOps</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("Main Menu")
        selected = st.radio(
            "Navigate",
            options=[
                "🏢 Business Overview",
                "📊 Analytics",
                "✨ Fick AI",
                "💾 Datasets",
                "💼 Workspaces",
                "⚙️ Settings",
                "❓ Help"
            ],
            index=0,
            key="nav"
        )

        st.markdown("---")
        if st.session_state.get("user"):
            user = st.session_state.user
            st.markdown(f"**{user.get('full_name','User')}**")
            st.markdown(f"_{user.get('email','')}_")
            if st.button("Logout"):
                for k in list(st.session_state.keys()):
                    st.session_state.pop(k, None)
                st.experimental_rerun()

def render_header():
    """Render a simple top header bar"""
    cols = st.columns([3, 1])
    with cols[0]:
        st.markdown("<div style='display:flex; align-items:center; gap:0.5rem;'><h2 style='margin:0'>📊 FiberOps</h2><div style='color:#9CA3AF'>Business Intelligence</div></div>", unsafe_allow_html=True)
    with cols[1]:
        if st.session_state.get("user"):
            st.button("🔔")
            st.button("⚙️")
