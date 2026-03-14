#!/usr/bin/env python3
"""
导入 database/camp.csv 到 camps 表，并清空原有数据。
导入后可在 Admin 后台编辑和更新这些营地。
使用方式（在项目根目录）:
  export PGPASSWORD=camppass
  python3 database/import_camp_csv.py
或:
  PGPASSWORD=camppass python3 database/import_camp_csv.py
"""
import csv
import os
import sys

try:
    import psycopg2
except ImportError:
    print("请先安装: pip install psycopg2-binary", file=sys.stderr)
    sys.exit(1)

# 与 backend 一致的数据库连接
DB = {
    "host": os.environ.get("POSTGRES_HOST", "localhost"),
    "port": os.environ.get("POSTGRES_PORT", "5432"),
    "dbname": os.environ.get("POSTGRES_DB", "camps"),
    "user": os.environ.get("POSTGRES_USER", "campuser"),
    "password": os.environ.get("POSTGRES_PASSWORD", "camppass"),
}

# 脚本所在目录 = database/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "camp.csv")


def norm_price(v):
    if not v or not str(v).strip():
        return 0.0
    s = str(v).strip().replace("$", "").replace(",", "")
    try:
        return float(s)
    except ValueError:
        return 0.0


def norm_str(v, max_len=None):
    if v is None:
        return None
    s = str(v).strip()
    if not s:
        return None
    if max_len and len(s) > max_len:
        return s[:max_len]
    return s


def norm_float(v):
    if v is None or not str(v).strip():
        return None
    try:
        return float(str(v).strip().replace(",", ""))
    except ValueError:
        return None


def main():
    if not os.path.isfile(CSV_PATH):
        print(f"找不到文件: {CSV_PATH}", file=sys.stderr)
        sys.exit(1)

    rows = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            price = norm_price(row.get("price"))
            tag = norm_str(row.get("tag"))
            if tag and tag.lower() not in ("popular", "new", "favourite"):
                tag = None
            rows.append({
                "name": (norm_str(row.get("name")) or "")[:255],
                "organization": norm_str(row.get("organization"), 255),
                "age_min": int(row.get("age_min") or 0),
                "age_max": int(row.get("age_max") or 0),
                "start_date": norm_str(row.get("start_date")),
                "end_date": norm_str(row.get("end_date")),
                "time_start": norm_str(row.get("time_start"), 20),
                "time_end": norm_str(row.get("time_end"), 20),
                "price": price,
                "category": norm_str(row.get("category"), 100),
                "address": (norm_str(row.get("address")) or "")[:500],
                "latitude": norm_float(row.get("latitude")),
                "longitude": norm_float(row.get("longitude")),
                "registration_link": norm_str(row.get("registration_link"), 500),
                "days_of_week": norm_str(row.get("days_of_week"), 100),
                "description": norm_str(row.get("description")),
                "image_url": norm_str(row.get("image_url"), 500),
                "tag": (tag or "")[:50] if tag else None,
            })

    if not rows:
        print("CSV 中没有数据行。")
        return

    conn = psycopg2.connect(**DB)
    cur = conn.cursor()
    try:
        cur.execute("TRUNCATE TABLE camps RESTART IDENTITY;")
        for r in rows:
            cur.execute(
                """
                INSERT INTO camps (
                    name, organization, age_min, age_max, start_date, end_date,
                    time_start, time_end, price, category, address, latitude, longitude,
                    registration_link, days_of_week, description, image_url, tag
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    r["name"], r["organization"], r["age_min"], r["age_max"],
                    r["start_date"], r["end_date"], r["time_start"], r["time_end"],
                    r["price"], r["category"], r["address"], r["latitude"], r["longitude"],
                    r["registration_link"], r["days_of_week"], r["description"],
                    r["image_url"], r["tag"],
                ),
            )
        conn.commit()
        print(f"已导入 {len(rows)} 条营地数据。可在 Admin 后台编辑和更新。")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
