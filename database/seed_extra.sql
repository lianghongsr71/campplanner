-- 额外营地数据：可随时执行，在下面继续添加更多 INSERT 即可。
-- 执行: PGPASSWORD=camppass psql -h localhost -U campuser -d camps -f database/seed_extra.sql
--
-- 字段说明: name, organization, age_min, age_max, price, address, category, tag, image_url
-- tag 可选: 'popular' | 'new' | 'favourite' 或 NULL
-- image_url 可选: 图片地址 或 占位色如 '#ea580c' 或 NULL

INSERT INTO camps (name, organization, age_min, age_max, price, address, category, tag, image_url) VALUES
  ('Easter Seals NL Day Camp', 'Easter Seals Newfoundland & Labrador', 6, 16, 125, '206 Mount Scio Road, St. John''s, NL', 'general / themed weekly', 'favourite', '#7c3aed');
-- 在下面继续添加，例如：
--   ('营地名', '机构', 最小年龄, 最大年龄, 价格, '地址', '类别', 'popular/new/favourite或NULL', '#颜色或NULL'),
--   (...),
