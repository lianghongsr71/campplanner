-- One-time init: create camps table and add image_url/tag. Safe to run multiple times.
--
-- 表结构与 Admin 管理后台、后端 API 完全一致，对应关系如下：
--
--   camps 表字段              Admin 表单 / API
--   -----------------------  ----------------------------------------
--   id (自增)                 自动生成，编辑时用
--   name                      Camp name *
--   organization              Organization
--   age_min                   Min age *
--   age_max                   Max age *
--   start_date                Start date
--   end_date                  End date
--   time_start                Time start
--   time_end                  Time end
--   price                     Price (CAD) *
--   category                  Category
--   address                   Address *
--   latitude                  Latitude
--   longitude                 Longitude
--   registration_link         Registration link
--   days_of_week              Days of week
--   description               Description
--   image_url                 Image URL or color
--   tag                       Tag (popular / new / favourite)
--   created_at               自动生成
--

CREATE TABLE IF NOT EXISTS camps (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    organization VARCHAR(255),
    age_min INTEGER NOT NULL CHECK (age_min >= 0),
    age_max INTEGER NOT NULL CHECK (age_max >= age_min),
    start_date DATE,
    end_date DATE,
    time_start VARCHAR(20),
    time_end VARCHAR(20),
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    category VARCHAR(100),
    address VARCHAR(500) NOT NULL,
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6),
    registration_link VARCHAR(500),
    days_of_week VARCHAR(100),
    description TEXT,
    image_url VARCHAR(500),
    tag VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add columns if table already existed without them (e.g. from older schema)
ALTER TABLE camps ADD COLUMN IF NOT EXISTS image_url VARCHAR(500);
ALTER TABLE camps ADD COLUMN IF NOT EXISTS tag VARCHAR(50);

-- ========== 三条示例营地数据（仅当表为空时插入）==========
-- 想继续在文件里加更多条，请用 database/seed_extra.sql，然后执行：
--   PGPASSWORD=camppass psql -h localhost -U campuser -d camps -f database/seed_extra.sql
INSERT INTO camps (name, organization, age_min, age_max, price, address, category, tag, image_url)
SELECT * FROM (VALUES
  ('Summer Sports Academy', 'St. John''s Recreation', 7, 14, 325, 'Bannerman Park, St. John''s, NL', 'sports', 'popular', '#ea580c'),
  ('Fun on the Water Youth Camp', 'City of St. John''s Recreation', 12, 15, 160, 'Rotary Park, St. John''s, NL', 'outdoor/sports', 'new', '#0ea5e9'),
  ('St. John''s Legends Summer Swim Camp', 'St. John''s Legends Swim Club', 5, 12, 200, 'Memorial University Pool, St. John''s, NL', 'swimming', NULL, '#06b6d4')
) AS v(name, organization, age_min, age_max, price, address, category, tag, image_url)
WHERE (SELECT COUNT(*) FROM camps) = 0;
