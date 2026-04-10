-- New camps batch 2 — insert if name not already in DB
INSERT INTO camps (
    name, organization, age_min, age_max, start_date, end_date,
    time_start, time_end, price, category, address,
    registration_link, days_of_week, description, tag
)
SELECT v.name, v.organization, v.age_min, v.age_max, v.start_date::DATE, v.end_date::DATE,
       v.time_start, v.time_end, v.price, v.category, v.address,
       v.registration_link, v.days_of_week, v.description, v.tag
FROM (VALUES
  ('Little Farmer Summer Camp', 'Lester''s Farm Chalet', 4, 9, '2026-06-29', '2026-08-28',
   '09:00', '16:00', 250, 'Outdoor', '173 Brookfield Rd, St. John''s, NL',
   'https://www.lestersfarmmarket.com/', 'Mon-Fri',
   'Hands-on farm experience for young children including animals and outdoor play.', 'popular'),

  ('Future Farmer Summer Camp', 'Lester''s Family Farm', 10, 15, '2026-06-29', '2026-08-28',
   '09:00', '16:00', 250, 'Outdoor', '173 Brookfield Rd, St. John''s, NL',
   'https://www.lestersfarmmarket.com/', 'Mon-Fri',
   'Advanced farm camp with responsibility, agriculture learning, and outdoor activities.', 'popular'),

  ('Mount Pearl Junior Day Camp', 'City of Mount Pearl', 5, 8, '2025-07-02', '2025-08-29',
   '08:30', '16:30', 140, 'Day Camp', 'Mount Pearl, NL',
   'https://www.mountpearl.ca/recreation/programs/day-camps/', 'Mon-Fri',
   'City-run day camp with games, crafts, and outdoor activities for younger children.', 'popular'),

  ('Mount Pearl Senior Day Camp', 'City of Mount Pearl', 9, 12, '2025-07-02', '2025-08-29',
   '08:30', '16:30', 140, 'Day Camp', 'Mount Pearl, NL',
   'https://www.mountpearl.ca/recreation/programs/day-camps/', 'Mon-Fri',
   'City-run camp with sports, trips, and group activities for older kids.', 'popular'),

  ('Botanical Explorers Camp', 'MUN Botanical Garden', 5, 8, '2026-06-30', '2026-08-31',
   '09:00', '16:00', 188, 'Outdoor', '306 Mt Scio Rd, St. John''s, NL',
   'https://www.mun.ca/botanicalgarden/learn/summer-camp/', 'Mon-Fri',
   'Nature exploration camp including plants, insects, and outdoor discovery.', 'favourite'),

  ('Eco Adventure Camp', 'MUN Botanical Garden', 9, 12, '2026-06-30', '2026-08-31',
   '09:00', '16:00', 188, 'Outdoor', '306 Mt Scio Rd, St. John''s, NL',
   'https://www.mun.ca/botanicalgarden/learn/summer-camp/', 'Mon-Fri',
   'Outdoor adventure and environmental learning camp with hands-on activities.', 'favourite'),

  ('Camp Whatchamacallit Junior', 'Aquarena / Field House', 5, 8, '2025-07-01', '2025-08-29',
   '09:00', '16:00', 200, 'Multi-Sport', '230 Elizabeth Ave, St. John''s, NL',
   'https://www.theworksonline.ca/events-listing/camp-whatchamacallit.php', 'Mon-Fri',
   'Multi-sport and recreational activities camp in Aquarena facilities.', 'popular'),

  ('Camp Whatchamacallit Senior', 'Aquarena / Field House', 9, 12, '2025-07-01', '2025-08-29',
   '09:00', '16:00', 200, 'Multi-Sport', '230 Elizabeth Ave, St. John''s, NL',
   'https://www.theworksonline.ca/events-listing/camp-whatchamacallit.php', 'Mon-Fri',
   'Sports, swimming, and group activities for older children.', 'popular'),

  ('Horseback Riding Camp Beginner', 'Bridle Path Stables', 6, 10, '2025-07-01', '2025-08-31',
   '09:00', '16:00', 350, 'Outdoor', 'Portugal Cove-St. Philip''s, NL',
   'https://bridlepathstable.ca/camps', 'Mon-Fri',
   'Introduction to horseback riding and horse care for beginners.', 'favourite'),

  ('Horseback Riding Camp Advanced', 'Bridle Path Stables', 11, 16, '2025-07-01', '2025-08-31',
   '09:00', '16:00', 350, 'Outdoor', 'Portugal Cove-St. Philip''s, NL',
   'https://bridlepathstable.ca/camps', 'Mon-Fri',
   'Advanced riding skills and horse management training.', 'favourite'),

  ('Gymnastics Camp Junior', 'Campia Gymnastics', 4, 7, '2025-07-01', '2025-08-29',
   '09:00', '16:00', 220, 'Gymnastics', '21 Old Placentia Rd, Mount Pearl, NL',
   'http://www.campia.ca/', 'Mon-Fri',
   'Basic gymnastics and fun activities for younger children.', 'popular'),

  ('Gymnastics Camp Senior', 'Campia Gymnastics', 8, 12, '2025-07-01', '2025-08-29',
   '09:00', '16:00', 220, 'Gymnastics', '21 Old Placentia Rd, Mount Pearl, NL',
   'http://www.campia.ca/', 'Mon-Fri',
   'Skill development gymnastics camp for older children.', 'popular'),

  ('YMCA Day Camp Junior', 'YMCA Newfoundland and Labrador', 5, 8, '2025-06-30', '2025-08-22',
   '08:00', '17:00', 125, 'Day Camp', '35 Ridge Rd, St. John''s, NL',
   'https://ymcanl.com/program/day-camps/', 'Mon-Fri',
   'General day camp with games, swimming, and social activities.', 'popular'),

  ('YMCA Day Camp Senior', 'YMCA Newfoundland and Labrador', 9, 12, '2025-06-30', '2025-08-22',
   '08:00', '17:00', 125, 'Day Camp', '35 Ridge Rd, St. John''s, NL',
   'https://ymcanl.com/program/day-camps/', 'Mon-Fri',
   'Expanded activities including leadership and group challenges.', 'popular'),

  ('Art Explorers Camp', 'The Rooms', 6, 9, '2026-07-01', '2026-08-15',
   '09:00', '16:00', 275, 'Arts', '9 Bonaventure Ave, St. John''s, NL',
   'https://therooms.ca/2026-summer-camps-rooms', 'Mon-Fri',
   'Creative art camp exploring painting, crafts, and museum exhibits.', 'favourite'),

  ('Creative Studio Camp', 'The Rooms', 10, 14, '2026-07-01', '2026-08-15',
   '09:00', '16:00', 275, 'Arts', '9 Bonaventure Ave, St. John''s, NL',
   'https://therooms.ca/2026-summer-camps-rooms', 'Mon-Fri',
   'Advanced art techniques and creative expression for older youth.', 'favourite'),

  ('Messy Art Camp Junior', 'Get Messy NL', 5, 8, '2025-07-01', '2025-08-15',
   '09:00', '15:00', 200, 'Arts', 'St. John''s, NL',
   'https://getmessynl.com/summer-camp-registration/', 'Mon-Fri',
   'Sensory and messy art camp focused on creativity and exploration.', 'popular'),

  ('Messy Art Camp Senior', 'Get Messy NL', 9, 12, '2025-07-01', '2025-08-15',
   '09:00', '15:00', 200, 'Arts', 'St. John''s, NL',
   'https://getmessynl.com/summer-camp-registration/', 'Mon-Fri',
   'Creative art projects and mixed media exploration.', 'popular'),

  ('Code Ninjas Jr Camp', 'Code Ninjas Mount Pearl', 5, 7, '2025-07-01', '2025-08-31',
   '09:00', '15:00', 250, 'Tech', 'Mount Pearl, NL',
   'https://www.codeninjas.com/mount-pearl-ca/camps', 'Mon-Fri',
   'Introductory coding camp with games and basic programming concepts.', 'new'),

  ('Code Ninjas Create Camp', 'Code Ninjas Mount Pearl', 8, 14, '2025-07-01', '2025-08-31',
   '09:00', '15:00', 250, 'Tech', 'Mount Pearl, NL',
   'https://www.codeninjas.com/mount-pearl-ca/camps', 'Mon-Fri',
   'Game development and coding projects for kids.', 'new'),

  ('Multi-Sport Camp Junior', 'Premier Sports Academy', 5, 8, '2025-07-01', '2025-08-29',
   '09:00', '16:00', 220, 'Multi-Sport', 'St. John''s, NL',
   'https://premiersportsacademy.ca/summer-camp', 'Mon-Fri',
   'Multi-sport introduction camp for younger children.', 'popular'),

  ('Elite Sports Camp', 'Premier Sports Academy', 9, 14, '2025-07-01', '2025-08-29',
   '09:00', '16:00', 220, 'Multi-Sport', 'St. John''s, NL',
   'https://premiersportsacademy.ca/summer-camp', 'Mon-Fri',
   'Skill development camp with structured training programs.', 'popular')

) AS v(name, organization, age_min, age_max, start_date, end_date,
       time_start, time_end, price, category, address,
       registration_link, days_of_week, description, tag)
WHERE NOT EXISTS (SELECT 1 FROM camps WHERE camps.name = v.name AND camps.organization = v.organization);
