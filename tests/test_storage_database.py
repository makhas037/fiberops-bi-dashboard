import io
import types
import pytest

from services.database import DatabaseService


class DummyStorage:
    def __init__(self):
        self.uploads = {}

    def from_(self, bucket):
        self._bucket = bucket
        return self

    def upload(self, key, bio):
        bio.seek(0)
        self.uploads[key] = bio.read()
        return {"message": "ok"}


class DummyTable:
    def __init__(self):
        self.rows = []

    def insert(self, meta):
        self.rows.append(meta)
        class Res:
            def __init__(self, data):
                self.data = data

            def execute(self):
                return types.SimpleNamespace(data=self.data)

        return Res([meta])


class DummyClient:
    def __init__(self):
        self.storage = DummyStorage()
        self._table = DummyTable()

    def table(self, name):
        return self._table


def test_add_dataset_csv(monkeypatch):
    # create a fake client with storage and table
    client = DummyClient()
    ds = DatabaseService(supabase_client=client)
    # monkeypatch None client behavior
    ds.client = client

    csv = "a,b\n1,2\n3,4\n"
    bio = io.BytesIO(csv.encode())
    res = ds.add_dataset("u1", bio, "test.csv", bucket="datasets")
    assert res["success"] is True
    assert res["meta"]["file_name"] == "test.csv"
