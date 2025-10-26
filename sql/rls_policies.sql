-- Recommended DDL and RLS policies for FiberOps datasets and profiles

-- Table: profiles (stores user metadata)
CREATE TABLE IF NOT EXISTS public.profiles (
  id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id uuid NOT NULL,
  full_name text,
  avatar_url text,
  created_at timestamptz DEFAULT timezone('utc'::text, now())
);

-- Table: datasets
CREATE TABLE IF NOT EXISTS public.datasets (
  id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id uuid NOT NULL,
  file_name text NOT NULL,
  storage_path text NOT NULL,
  file_size bigint,
  row_count integer,
  column_names jsonb,
  created_at timestamptz DEFAULT timezone('utc'::text, now())
);

-- Example: allow authenticated users to insert their own profile
-- (Assumes auth.uid() returns a uuid or text that matches user_id)
DROP POLICY IF EXISTS insert_own_profile ON public.profiles;
CREATE POLICY insert_own_profile ON public.profiles
  FOR INSERT
  WITH CHECK (
    auth.uid()::text = user_id::text
  );

-- Allow users to select/update their own profile
DROP POLICY IF EXISTS select_own_profile ON public.profiles;
CREATE POLICY select_own_profile ON public.profiles
  FOR SELECT
  USING (
    auth.uid()::text = user_id::text
  );

DROP POLICY IF EXISTS update_own_profile ON public.profiles;
CREATE POLICY update_own_profile ON public.profiles
  FOR UPDATE
  USING (
    auth.uid()::text = user_id::text
  )
  WITH CHECK (
    auth.uid()::text = user_id::text
  );

-- Datasets RLS: allow users to manage their own dataset metadata
DROP POLICY IF EXISTS select_own_datasets ON public.datasets;
CREATE POLICY select_own_datasets ON public.datasets
  FOR SELECT
  USING (
    auth.uid()::text = user_id::text
  );

DROP POLICY IF EXISTS insert_own_datasets ON public.datasets;
CREATE POLICY insert_own_datasets ON public.datasets
  FOR INSERT
  WITH CHECK (
    auth.uid()::text = user_id::text
  );

DROP POLICY IF EXISTS delete_own_datasets ON public.datasets;
CREATE POLICY delete_own_datasets ON public.datasets
  FOR DELETE
  USING (
    auth.uid()::text = user_id::text
  );

-- Notes:
-- - If your auth.uid() returns text, adjust casting appropriately. The explicit ::text casts avoid operator mismatch errors.
-- - For storage bucket access, consider server-side uploads using the SERVICE_ROLE key and keep the bucket private.
-- - To generate uuid functions in Supabase/Postgres enable the extension (superuser required):
--     create extension if not exists "uuid-ossp";

*** End Patch