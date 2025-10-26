# FiberOps BI Dashboard

This repository is a Streamlit-based BI platform scaffold (FiberOps). It includes authentication, dataset management, analytics pages and an AI assistant integration.

Quick start (development)

1. Copy `.streamlit/secrets.toml` (or create a `.env`) and fill your Supabase and API keys.

2. Create a Python virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run streamlit_app.py
```

Notes
- The app expects Supabase credentials. For server-side dataset uploads the `service_role_key` (SUPABASE_SERVICE_KEY) is used.
- Keep `.streamlit/secrets.toml` out of version control — it contains secret keys.
- See `sql/rls_policies.sql` for recommended RLS and table definitions.

Environment variables (examples)

You can either use `.streamlit/secrets.toml` or a `.env` file (or platform secrets). A `.env.example` has been added at the project root. Key names used by the app:

- SUPABASE_URL — your Supabase project URL (https://<project>.supabase.co)
- SUPABASE_ANON_KEY — the anon/public key (for client-side limited actions)
- SUPABASE_SERVICE_KEY — the service role key (server-side admin operations, keep private)
- GEMINI_API_KEY — Google Generative AI / Gemini key used by Fick AI (if enabled)
- STRIPE_PUBLISHABLE_KEY / STRIPE_SECRET_KEY — Stripe keys for billing
- SMTP_HOST / SMTP_PORT / SMTP_USER / SMTP_PASS — optional email settings for transactional emails
- JWT_SECRET — optional secret used for app-level token generation

Security

- Never commit service keys (`SUPABASE_SERVICE_KEY`, `STRIPE_SECRET_KEY`, etc.) to source control.
- Use Streamlit Cloud secrets, Vault, or environment variables in production.

Remember-me behavior (dev)

- The app implements a simple "remember me" convenience for development: when you check "Remember me" at login the session tokens are saved to a local file named `.auth_session.json` in the project root.
- This file is not encrypted — treat it as sensitive. In production use secure session storage (Redis, encrypted cookies, or the hosting platform's secrets).


Security and deployment
- In production, use a secrets manager (Streamlit Cloud secrets, AWS Secrets Manager, etc.)
- Rotate keys regularly. Use the service role key only server-side.

Contact
- For help, open an issue in the repo or contact the maintainer.
# FiberOps BI Platform (scaffold)

This workspace is a scaffold for the FiberOps Business Intelligence Streamlit application.

Quick start (development):

1. Create and fill `.env` (recommended: copy `.env.example` and set SUPABASE_URL and keys).
2. Create and activate a virtualenv:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run streamlit_app.py
```

Notes:
- This scaffold includes minimal pages and a `DatabaseService` that uses `supabase` client. Configure Supabase keys to enable storage/profile operations.
- Pages are located under `pages/` and components under `components/`.
