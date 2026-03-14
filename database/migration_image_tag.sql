-- Add image_url and tag to camps (run if table already exists)
ALTER TABLE camps ADD COLUMN IF NOT EXISTS image_url VARCHAR(500);
ALTER TABLE camps ADD COLUMN IF NOT EXISTS tag VARCHAR(50);
