import os
from typing import Optional

try:
    import google.generativeai as genai
except Exception:
    genai = None


def init_client(api_key: Optional[str] = None):
    key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not key:
        return None
    if genai is None:
        raise RuntimeError("google-generativeai package not installed")
    genai.configure(api_key=key)
    return genai


def generate_text(prompt: str, max_output_tokens: int = 512, model: str = "models/text-bison-001") -> str:
    """Generate text using Gemini (Google generative AI).

    Returns the generated text. Raises RuntimeError if client not configured.
    """
    client = init_client()
    if not client:
        raise RuntimeError("GEMINI API key not configured (set GEMINI_API_KEY in env or streamlit secrets)")

    resp = client.generate_text(model=model, prompt=prompt, max_output_tokens=max_output_tokens)
    # The shape depends on the library version; try to extract text safely
    try:
        return resp.text
    except Exception:
        # Fallback: try first candidate
        try:
            return resp.candidates[0].content
        except Exception:
            return str(resp)
import os

class GeminiAI:
    """Placeholder Gemini AI integration.

    Replace the internals with real calls to Google Generative APIs when you
    provide `GEMINI_API_KEY` in Streamlit secrets or environment.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

    def available(self) -> bool:
        return bool(self.api_key)

    def generate_text(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY not configured")
        # placeholder synchronous response
        return f"[gemini stub] response to: {prompt}"

    def stream_text(self, prompt: str):
        # yields chunks for streaming UI
        for i in range(1, 4):
            yield f"chunk {i} for: {prompt}"
