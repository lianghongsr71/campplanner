-- Migration: add camp_sessions table + update favorites
-- Run once on existing DB:
--   sudo docker cp database/migration_sessions.sql summer-camp-platform-postgres-1:/tmp/m.sql
--   sudo docker exec summer-camp-platform-postgres-1 psql -U campuser -d camps -f /tmp/m.sql

-- 1. Camp sessions table
CREATE TABLE IF NOT EXISTS camp_sessions (
    id            SERIAL PRIMARY KEY,
    camp_id       INTEGER NOT NULL REFERENCES camps(id) ON DELETE CASCADE,
    week_number   INTEGER NOT NULL,
    label         VARCHAR(100),
    start_date    DATE NOT NULL,
    end_date      DATE NOT NULL,
    price_per_week DECIMAL(10,2),
    created_at    TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (camp_id, week_number)
);

-- 2. Add session_id to favorites (keep existing rows intact, session_id = NULL)
ALTER TABLE favorites ADD COLUMN IF NOT EXISTS session_id INTEGER REFERENCES camp_sessions(id) ON DELETE CASCADE;

-- 3. Drop old PK, add new flexible unique constraint
ALTER TABLE favorites DROP CONSTRAINT IF EXISTS favorites_pkey;
ALTER TABLE favorites DROP CONSTRAINT IF EXISTS favorites_user_uuid_camp_id_session_id_key;

-- New surrogate PK so we can have (user, camp) + (user, session) both
ALTER TABLE favorites ADD COLUMN IF NOT EXISTS fav_id SERIAL;
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint WHERE conname = 'favorites_pkey'
  ) THEN
    ALTER TABLE favorites ADD PRIMARY KEY (fav_id);
  END IF;
END$$;

-- Unique: one row per (user, camp, session) — session can be NULL
CREATE UNIQUE INDEX IF NOT EXISTS favorites_unique_session
    ON favorites (user_uuid, camp_id, COALESCE(session_id, -1));
