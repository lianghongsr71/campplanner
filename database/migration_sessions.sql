-- Migration: add camp_sessions table + create/update favorites
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

-- 2. Create favorites with new schema if it doesn't exist at all
CREATE TABLE IF NOT EXISTS favorites (
    fav_id     SERIAL PRIMARY KEY,
    user_uuid  VARCHAR(36) NOT NULL,
    camp_id    INTEGER NOT NULL REFERENCES camps(id) ON DELETE CASCADE,
    session_id INTEGER REFERENCES camp_sessions(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. If favorites already existed with old schema, add missing columns
ALTER TABLE favorites ADD COLUMN IF NOT EXISTS fav_id SERIAL;
ALTER TABLE favorites ADD COLUMN IF NOT EXISTS session_id INTEGER REFERENCES camp_sessions(id) ON DELETE CASCADE;

-- 4. Ensure fav_id is the primary key (safe if already set)
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint WHERE conname = 'favorites_pkey'
  ) THEN
    ALTER TABLE favorites ADD PRIMARY KEY (fav_id);
  END IF;
END$$;

-- 5. Unique: one row per (user, camp, session)
CREATE UNIQUE INDEX IF NOT EXISTS favorites_unique_session
    ON favorites (user_uuid, camp_id, COALESCE(session_id, -1));
