import streamlit as st
from services.gemini_ai import generate_text


def render():
    st.header("✨ Fick AI")
    st.write("Ask Fick AI to summarize data, generate insights, or craft text.")

    if not st.secrets.get("gemini", {}).get("api_key") and not st.session_state.get("GEMINI_API_KEY"):
        st.warning("GEMINI API key not configured. Add it to .streamlit/secrets.toml as [gemini] api_key = \"...\" or set GEMINI_API_KEY in the environment.")
        return

    prompt = st.text_area("Enter your prompt", height=200)
    model = st.selectbox("Model", options=["models/text-bison-001"], index=0)
    if st.button("Generate"):
        if not prompt.strip():
            st.error("Please enter a prompt")
        else:
            with st.spinner("Generating..."):
                try:
                    text = generate_text(prompt, model=model)
                    st.success("Generated")
                    st.write(text)
                except Exception as e:
                    st.error(f"Generation failed: {e}")
