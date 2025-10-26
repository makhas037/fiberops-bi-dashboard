#!/usr/bin/env bash
# Run SQL files against a Postgres connection. Intended for Supabase projects.
# Usage: PG_CONN=postgres://user:pass@host:port/db ./scripts/run_sql.sh sql/rls_user_sessions.sql

set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: PG_CONN=postgres://... $0 <sql-file1> [sql-file2 ...]"
  exit 2
fi

if [ -z "${PG_CONN:-}" ]; then
  echo "Please set PG_CONN environment variable to a Postgres connection string (e.g. from Supabase)."
  exit 2
fi

for f in "$@"; do
  if [ ! -f "$f" ]; then
    echo "SQL file not found: $f"
    exit 2
  fi
  echo "Running $f ..."
  psql "$PG_CONN" -f "$f"
done

echo "All done."
