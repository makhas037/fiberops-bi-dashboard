import types
import pytest

import utils.auth as auth_module


def make_session_store():
    store = {}

    def set_session_value(k, v):
        store[k] = v

    def get_session_value(k):
        return store.get(k)

    def clear_session():
        store.clear()

    return store, set_session_value, get_session_value, clear_session


class FakeAuth:
    def __init__(self):
        self.signed_out = False

    def sign_in_with_password(self, payload):
        # simulate supabase-py style response
        return {
            "data": {
                "user": {"id": "u1", "email": payload.get("email")},
                "session": {"access_token": "tok1", "refresh_token": "ref1"},
            }
        }

    def sign_out(self):
        self.signed_out = True

    def reset_password_for_email(self, email):
        return {"data": "ok"}


class FakeClient:
    def __init__(self):
        self.auth = FakeAuth()


class FakeDB:
    def __init__(self, client=None):
        self._client = client

    def get_user_profile(self, uid):
        return {"user_id": uid, "full_name": "Test User"}


def test_login_user_success(monkeypatch):
    store, set_session_value, get_session_value, clear_session = make_session_store()

    monkeypatch.setattr(auth_module, "get_supabase_client", lambda: FakeClient())
    monkeypatch.setattr(auth_module, "DatabaseService", lambda client=None: FakeDB(client))
    monkeypatch.setattr(auth_module, "set_session_value", set_session_value)
    monkeypatch.setattr(auth_module, "get_session_value", get_session_value)
    monkeypatch.setattr(auth_module, "clear_session", clear_session)

    ok, msg = auth_module.login_user("a@b.com", "pw123", remember_me=False)
    assert ok is True
    assert store.get("authenticated") is True
    assert store.get("user")["email"] == "a@b.com"
    assert store.get("auth_token") == "tok1"


def test_logout_user(monkeypatch):
    # prepare fake client and session
    fake_client = FakeClient()
    store, set_session_value, get_session_value, clear_session = make_session_store()
    store["foo"] = "bar"

    monkeypatch.setattr(auth_module, "get_supabase_client", lambda: fake_client)
    monkeypatch.setattr(auth_module, "clear_session", clear_session)

    auth_module.logout_user()
    assert store == {}
    assert fake_client.auth.signed_out is True


def test_reset_password(monkeypatch):
    monkeypatch.setattr(auth_module, "get_supabase_client", lambda: FakeClient())
    ok, msg = auth_module.reset_password("a@b.com")
    assert ok is True


def test_check_authentication_calls_timeout(monkeypatch):
    # ensure get_session_value("authenticated") returns True
    monkeypatch.setattr(auth_module, "get_session_value", lambda k: True if k == "authenticated" else None)
    import utils.session as session_mod

    monkeypatch.setattr(session_mod, "check_session_timeout", lambda: True)

    assert auth_module.check_authentication() is True
