SQL_FILES := sql/rls_user_sessions.sql sql/enable_rls_user_sessions.sql

.PHONY: run-sql
run-sql:
	@echo "Run SQL files against PG_CONN"
	@if [ -z "${PG_CONN}" ]; then \
	  echo "Set PG_CONN environment variable first (postgres://user:pass@host:port/db)"; exit 2; \
	fi
	./scripts/run_sql.sh $(SQL_FILES)

.PHONY: create-user-sessions
create-user-sessions:
	@echo "Run Python helper to create user_sessions using PG_CONN or SUPABASE_DB_CONN"
	@if [ -z "${PG_CONN}" ] && [ -z "${SUPABASE_DB_CONN}" ]; then \
	  echo "Set PG_CONN or SUPABASE_DB_CONN environment variable first"; exit 2; \
	fi
	./scripts/create_user_sessions.py
