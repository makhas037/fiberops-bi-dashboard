-- Enable RLS and create policies for user_sessions
-- Run this AFTER creating the table (see rls_user_sessions.sql)

-- NOTE: before running these commands, ensure your DB allows running ALTER TABLE and POLICY statements.

-- Enable row level security
alter table if exists public.user_sessions enable row level security;

-- Allow the service role (supabase service key) to INSERT rows.
-- We detect service role by checking the presence of a custom claim `role` = 'service_role'
-- If your supabase setup uses a different claim, adjust accordingly.
create policy if not exists "Service role can insert" on public.user_sessions
  for insert
  with check (auth.role() = 'service_role');

-- Allow authenticated users to insert their own sessions (optional)
create policy if not exists "Users can insert own session" on public.user_sessions
  for insert
  with check (auth.uid() = user_id);

-- Allow users to select their own active sessions
create policy if not exists "Users can select own" on public.user_sessions
  for select
  using (auth.uid() = user_id AND expires_at > now());

-- Allow users to delete their own sessions
create policy if not exists "Users can delete own" on public.user_sessions
  for delete
  using (auth.uid() = user_id);

-- Optionally allow service role to delete (cleanup) expired sessions
create policy if not exists "Service role can delete" on public.user_sessions
  for delete
  using (auth.role() = 'service_role' OR auth.uid() = user_id);
