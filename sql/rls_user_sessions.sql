-- DDL and example RLS policies for the `user_sessions` table
-- Run this in your Supabase SQL editor (or psql) for the target project/schema.

-- Create table
create table if not exists public.user_sessions (
  id uuid default gen_random_uuid() primary key,
  user_id text not null,
  token text not null unique,
  expires_at timestamptz not null,
  created_at timestamptz default now()
);

-- Index to help lookups by token
create index if not exists idx_user_sessions_token on public.user_sessions (token);

-- Example: recommend using RLS to restrict who can read/write sessions
-- 1) Enable RLS
-- alter table public.user_sessions enable row level security;

-- 2) Policy: allow authenticated users to create sessions for themselves
-- (when using Supabase's built-in auth, `auth.uid()` is available in policies)
-- create policy "Allow insert own session" on public.user_sessions
--   for insert
--   with check (auth.uid() = user_id);

-- 3) Policy: allow users to read their own active sessions
-- -- create policy "Allow select own session" on public.user_sessions
-- --   for select
-- --   using (auth.uid() = user_id AND expires_at > now());

-- 4) Policy: allow users to delete their own sessions
-- create policy "Allow delete own session" on public.user_sessions
--   for delete
--   using (auth.uid() = user_id);

-- If you plan to handle session creation server-side (recommended), perform inserts
-- using the Service Role key from a secure server component. In that case you
-- may want to create a separate policy to allow the service role to insert rows
-- while still preventing client-side inserts from untrusted keys.

-- Example cleanup query (optional): remove expired sessions
-- delete from public.user_sessions where expires_at < now();

-- Note: gen_random_uuid() requires the pgcrypto extension. If not available use:
--   create extension if not exists "pgcrypto";
