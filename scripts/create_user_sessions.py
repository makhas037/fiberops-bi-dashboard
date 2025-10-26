#!/usr/bin/env python3
"""
Create the `user_sessions` table in a Postgres database using a connection string.

This script is useful when you cannot or prefer not to run psql directly. It reads
SQL from `sql/rls_user_sessions.sql` and `sql/enable_rls_user_sessions.sql` and executes
them in the target database.

Usage:
  PG_CONN=postgres://user:pass@host:5432/postgres ./scripts/create_user_sessions.py

If PG_CONN is not set, the script will try SUPABASE_DB_CONN (a full Postgres connection
string) as an alternative.

IMPORTANT: this script will run DDL. Use carefully and ensure you have backups.
"""
import os
import sys
from pathlib import Path

SQL_FILES = [
    Path(__file__).resolve().parents[1] / "sql" / "rls_user_sessions.sql",
    Path(__file__).resolve().parents[1] / "sql" / "enable_rls_user_sessions.sql",
]


def main():
    pg_conn = os.environ.get("PG_CONN") or os.environ.get("SUPABASE_DB_CONN")
    if not pg_conn:
        print("ERROR: Set PG_CONN (postgres://...) or SUPABASE_DB_CONN environment variable.")
        sys.exit(2)

    try:
        import psycopg2
    except Exception:
        print("Missing dependency: install psycopg2-binary: pip install psycopg2-binary")
        sys.exit(2)

    sql_text = "\n\n".join([f.read_text() for f in SQL_FILES if f.exists()])
    if not sql_text.strip():
        print("No SQL found in expected files:")
        for f in SQL_FILES:
            print(" -", f)
        sys.exit(2)

    print("Connecting to DB and running SQL...")
    conn = psycopg2.connect(pg_conn)
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute(sql_text)
        print("SQL executed successfully.")
    except Exception as e:
        print("Failed to execute SQL:", e)
        sys.exit(3)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
