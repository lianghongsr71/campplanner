-- 额外营地数据：可随时执行，在下面继续添加更多 INSERT 即可。
-- 执行: PGPASSWORD=camppass psql -h localhost -U campuser -d camps -f database/seed_extra.sql
--
-- 字段说明: name, organization, age_min, age_max, price, address, category, tag, image_url
-- tag 可选: 'popular' | 'new' | 'favourite' 或 NULL
-- image_url 可选: 图片地址 或 占位色如 '#ea580c' 或 NULL

INSERT INTO camps (name, organization, age_min, age_max, price, address, category, tag, image_url) VALUES
  ('Easter Seals NL Day Camp', 'Easter Seals Newfoundland & Labrador', 6, 16, 125, '206 Mount Scio Road, St. John''s, NL', 'general / themed weekly', 'favourite', '#7c3aed');

-- ── 2026-04-01 新增 10 条 ──────────────────────────────────────────
INSERT INTO camps
  (name, organization, age_min, age_max, start_date, end_date,
   time_start, time_end, price, category, address,
   latitude, longitude, registration_link, days_of_week, description, image_url, tag)
VALUES
  ('GC Sports Summer Camp', 'GC Sports Centre', 5, 12, '2025-07-01', '2025-08-29', '09:00', '16:00', 200, 'Multi-Sport', '8 Panther Pl, Mount Pearl, NL', NULL, NULL, 'https://www.gcsports.ca', 'Mon-Fri', 'Indoor and outdoor multi-sport camp, weather independent, suitable for young children.', NULL, 'popular'),
  ('Campia Gymnastics Summer Camp', 'Campia Gymnastics', 4, 12, '2025-07-01', '2025-08-29', '09:00', '16:00', 220, 'Gymnastics', '21 Old Placentia Rd, Mount Pearl, NL', NULL, NULL, 'http://www.campia.ca', 'Mon-Fri', 'Gymnastics and physical activity camp, ideal for energetic kids.', NULL, 'popular'),
  ('Little Gym Summer Camp', 'The Little Gym of St Johns', 3, 10, '2025-07-01', '2025-08-29', '09:00', '15:00', 210, 'Gymnastics', '286 Torbay Rd, St. John''s, NL', NULL, NULL, 'https://www.thelittlegym.com', 'Mon-Fri', 'Small group camp focused on gymnastics and confidence building.', NULL, 'favourite'),
  ('Cirque Arts Summer Camp', 'Cirque''letics School of Circus Arts', 6, 14, '2025-07-01', '2025-08-29', '09:00', '15:00', 230, 'Circus Arts', '60 O''Leary Ave, St. John''s, NL', NULL, NULL, 'http://cirqueletics.ca', 'Mon-Fri', 'Circus skills camp including aerial silks and acrobatics.', NULL, 'new'),
  ('Jelly Bean Themed Summer Camp', 'Jelly Bean Entertainment', 5, 12, '2025-07-01', '2025-08-15', '09:00', '16:00', 180, 'Entertainment', '430 Topsail Rd, St. John''s, NL', NULL, NULL, 'http://www.jellybeanentertainment.ca', 'Mon-Fri', 'Themed entertainment camp focused on games and fun activities.', NULL, NULL),
  ('Lakecrest Summer Camp', 'Lakecrest Independent School', 4, 12, '2025-07-01', '2025-08-29', '09:00', '16:00', 300, 'Academic & Outdoor', '58 Patrick St, St. John''s, NL', NULL, NULL, 'http://www.lakecrest.ca', 'Mon-Fri', 'Private school camp combining academics, outdoor play, and arts.', NULL, 'favourite'),
  ('Shallaway Music Camp', 'Shallaway Youth Choir', 6, 16, '2025-07-01', '2025-07-31', '09:00', '16:00', 250, 'Music', '20 Hallett Crescent, St. John''s, NL', NULL, NULL, 'http://www.shallaway.ca', 'Mon-Fri', 'Choral and music training camp with a focus on performance skills.', NULL, NULL),
  ('Shine Music Summer Camp', 'Shine Music', 5, 12, '2025-07-01', '2025-08-15', '09:00', '15:00', 200, 'Music & Arts', '59 Pippy Pl, St. John''s, NL', NULL, NULL, 'https://shinemusic.ca', 'Mon-Fri', 'Music and creative arts camp with small group instruction.', NULL, 'popular'),
  ('Whee Indoor Play Camp', 'Whee Indoor Games', 4, 10, '2025-07-01', '2025-08-15', '10:00', '15:00', 150, 'Indoor Play', 'St. John''s, NL', NULL, NULL, NULL, 'Mon-Fri', 'Indoor playground style supervised activities, not a formal camp.', NULL, NULL),
  ('St Johns Basketball Skills Camp', 'St Johns Minor Basketball', 8, 14, '2025-07-15', '2025-07-20', '09:00', '15:00', 180, 'Basketball', 'St. John''s, NL', NULL, NULL, NULL, 'Mon-Fri', 'Basketball skills development camp, not a recurring annual program.', NULL, NULL);

