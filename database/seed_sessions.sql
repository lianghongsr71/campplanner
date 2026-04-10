-- Test data: Little Farmer Summer Camp at Lester's Family Farm
-- Run after migration_sessions.sql

INSERT INTO camps (name, organization, age_min, age_max, start_date, end_date,
                   time_start, time_end, price, category, address,
                   registration_link, days_of_week, description, tag)
VALUES (
  'Little Farmer Summer Camp',
  'Lester''s Family Farm',
  4, 12,
  '2025-06-29', '2025-09-04',
  '09:00', '16:00',
  250.00,
  'Farm & Nature',
  'Lester''s Family Farm, Ottawa, ON',
  'https://www.lestersfamilyfarm.ca/farm-camp.php#!/Little-Farmer-Summer-Camp/p/100103074',
  'Mon-Fri',
  'Hands-on farm experience for kids: animal care, planting, outdoor exploration. Weekly sessions Jun-Sep.',
  'popular'
)
ON CONFLICT DO NOTHING;

-- Insert 10 weekly sessions for this camp
WITH camp AS (SELECT id FROM camps WHERE name = 'Little Farmer Summer Camp' LIMIT 1)
INSERT INTO camp_sessions (camp_id, week_number, label, start_date, end_date, price_per_week)
SELECT
  camp.id,
  w.week_number,
  'Week ' || w.week_number || ': ' || w.label,
  w.start_date::DATE,
  w.end_date::DATE,
  250.00
FROM camp, (VALUES
  (1, 'June 29 - July 3',      '2025-06-29', '2025-07-03'),
  (2, 'July 6 - July 10',      '2025-07-06', '2025-07-10'),
  (3, 'July 13 - July 17',     '2025-07-13', '2025-07-17'),
  (4, 'July 20 - July 24',     '2025-07-20', '2025-07-24'),
  (5, 'July 27 - July 31',     '2025-07-27', '2025-07-31'),
  (6, 'August 3 - August 7',   '2025-08-03', '2025-08-07'),
  (7, 'August 10 - August 14', '2025-08-10', '2025-08-14'),
  (8, 'August 17 - August 21', '2025-08-17', '2025-08-21'),
  (9, 'August 24 - August 28', '2025-08-24', '2025-08-28'),
  (10,'August 31 - September 4','2025-08-31','2025-09-04')
) AS w(week_number, label, start_date, end_date)
ON CONFLICT (camp_id, week_number) DO NOTHING;
