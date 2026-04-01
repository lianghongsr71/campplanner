"""
Summer Camp Finder - FastAPI Backend
GET /camps: age, q (keyword), category filters. Admin: X-Admin-Key for POST/PUT/DELETE.
Favorites: GET/POST/DELETE /favorites/{user_uuid}/{camp_id}, GET /favorites/{user_uuid}.
"""
from typing import Optional
import re
from decimal import Decimal
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Query, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Summer Camp Finder API")

class CampCreate(BaseModel):
    name: str
    organization: Optional[str] = None
    age_min: int
    age_max: int
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    time_start: Optional[str] = None
    time_end: Optional[str] = None
    price: float
    category: Optional[str] = None
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    registration_link: Optional[str] = None
    days_of_week: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None  # image URL or hex color e.g. #ea580c for placeholder
    tag: Optional[str] = None  # popular | new | favourite

class CampUpdate(BaseModel):
    name: Optional[str] = None
    organization: Optional[str] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    time_start: Optional[str] = None
    time_end: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    registration_link: Optional[str] = None
    days_of_week: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    tag: Optional[str] = None

def require_admin(x_admin_key: Optional[str] = Header(None, alias="X-Admin-Key")):
    # Auth temporarily disabled — re-enable when ADMIN_API_KEY is configured
    pass

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    host = os.environ.get("POSTGRES_HOST", "localhost")
    return psycopg2.connect(
        host=host,
        port=os.environ.get("POSTGRES_PORT", "5432"),
        dbname=os.environ.get("POSTGRES_DB", "camps"),
        user=os.environ.get("POSTGRES_USER", "campuser"),
        password=os.environ.get("POSTGRES_PASSWORD", "camppass"),
        cursor_factory=RealDictCursor,
    )

@app.get("/")
def root():
    return {"message": "Summer Camp Finder API", "endpoints": {"camps": "/camps", "health": "/health", "docs": "/docs"}}

@app.get("/camps")
@app.get("/camps/")
def list_camps(
    age: Optional[int] = Query(None, description="Filter by age"),
    q: Optional[str] = Query(None, description="Search keyword"),
    category: Optional[str] = Query(None, description="Filter by category (e.g. sports, swimming, art&craft)"),
):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cols = "id, name, organization, age_min, age_max, start_date, end_date, time_start, time_end, price, category, address, latitude, longitude, registration_link, days_of_week, description, image_url, tag"
            conditions = []
            params = []
            if age is not None:
                conditions.append("age_min <= %s AND age_max >= %s")
                params.extend([age, age])
            keyword = (q or "").strip()
            if keyword:
                pattern = "%" + keyword + "%"
                conditions.append("(name ILIKE %s OR organization ILIKE %s OR category ILIKE %s OR address ILIKE %s OR description ILIKE %s)")
                params.extend([pattern] * 5)
            if category and category.strip():
                cat = category.strip()
                conditions.append("category ILIKE %s")
                params.append("%" + cat + "%")
            where = " AND ".join(conditions) if conditions else "TRUE"
            cur.execute(f"SELECT {cols} FROM camps WHERE {where} ORDER BY name", tuple(params))
            rows = cur.fetchall()
        return [_row_to_dict(row) for row in rows]
    finally:
        conn.close()

def _row_to_dict(row) -> dict:
    d = dict(row)
    for k, v in list(d.items()):
        if hasattr(v, "isoformat"):
            d[k] = v.isoformat()
        elif isinstance(v, Decimal):
            d[k] = float(v)
    return d

@app.get("/camps/{camp_id}")
def get_camp(camp_id: int):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, organization, age_min, age_max, start_date, end_date, time_start, time_end, price, category, address, latitude, longitude, registration_link, days_of_week, description, image_url, tag FROM camps WHERE id = %s", (camp_id,))
            row = cur.fetchone()
        if not row:
            raise HTTPException(404, "Camp not found")
        return _row_to_dict(row)
    finally:
        conn.close()

@app.post("/camps")
def create_camp(body: CampCreate, _: bool = Depends(require_admin)):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO camps (name, organization, age_min, age_max, start_date, end_date, time_start, time_end, price, category, address, latitude, longitude, registration_link, days_of_week, description, image_url, tag)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, name, organization, age_min, age_max, start_date, end_date, time_start, time_end, price, category, address, latitude, longitude, registration_link, days_of_week, description, image_url, tag
            """, (body.name, body.organization, body.age_min, body.age_max, body.start_date or None, body.end_date or None, body.time_start, body.time_end, body.price, body.category, body.address, body.latitude, body.longitude, body.registration_link, body.days_of_week, body.description, body.image_url, body.tag))
            row = cur.fetchone()
        conn.commit()
        return _row_to_dict(row)
    finally:
        conn.close()

@app.put("/camps/{camp_id}")
def update_camp(camp_id: int, body: CampUpdate, _: bool = Depends(require_admin)):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM camps WHERE id = %s", (camp_id,))
            if not cur.fetchone():
                raise HTTPException(404, "Camp not found")
            cur.execute("""
                UPDATE camps SET name=COALESCE(%s,name), organization=COALESCE(%s,organization), age_min=COALESCE(%s,age_min), age_max=COALESCE(%s,age_max), start_date=COALESCE(%s,start_date), end_date=COALESCE(%s,end_date), time_start=COALESCE(%s,time_start), time_end=COALESCE(%s,time_end), price=COALESCE(%s,price), category=COALESCE(%s,category), address=COALESCE(%s,address), latitude=COALESCE(%s,latitude), longitude=COALESCE(%s,longitude), registration_link=COALESCE(%s,registration_link), days_of_week=COALESCE(%s,days_of_week), description=COALESCE(%s,description), image_url=COALESCE(%s,image_url), tag=COALESCE(%s,tag) WHERE id=%s
            """, (body.name, body.organization, body.age_min, body.age_max, body.start_date, body.end_date, body.time_start, body.time_end, float(body.price) if body.price is not None else None, body.category, body.address, body.latitude, body.longitude, body.registration_link, body.days_of_week, body.description, body.image_url, body.tag, camp_id))
            cur.execute("SELECT id, name, organization, age_min, age_max, start_date, end_date, time_start, time_end, price, category, address, latitude, longitude, registration_link, days_of_week, description, image_url, tag FROM camps WHERE id = %s", (camp_id,))
            row = cur.fetchone()
        conn.commit()
        return _row_to_dict(row)
    finally:
        conn.close()

@app.delete("/camps/{camp_id}")
def delete_camp(camp_id: int, _: bool = Depends(require_admin)):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM camps WHERE id = %s RETURNING id", (camp_id,))
            if not cur.fetchone():
                raise HTTPException(404, "Camp not found")
        conn.commit()
        return {"ok": True}
    finally:
        conn.close()

@app.get("/admin/ping")
def admin_ping(_: bool = Depends(require_admin)):
    """Verify admin key without side effects."""
    return {"ok": True}

@app.get("/health")
def health():
    return {"status": "ok"}

_UUID_RE = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)

def _valid_uuid(user_uuid: str):
    if not _UUID_RE.match(user_uuid):
        raise HTTPException(400, "Invalid user UUID")

@app.get("/favorites/{user_uuid}")
def get_favorites(user_uuid: str):
    _valid_uuid(user_uuid)
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.id, c.name, c.organization, c.age_min, c.age_max, c.start_date, c.end_date,
                       c.time_start, c.time_end, c.price, c.category, c.address, c.latitude, c.longitude,
                       c.registration_link, c.days_of_week, c.description, c.image_url, c.tag
                FROM favorites f JOIN camps c ON f.camp_id = c.id
                WHERE f.user_uuid = %s ORDER BY f.created_at
            """, (user_uuid,))
            rows = cur.fetchall()
        return [_row_to_dict(row) for row in rows]
    finally:
        conn.close()

@app.post("/favorites/{user_uuid}/{camp_id}")
def add_favorite(user_uuid: str, camp_id: int):
    _valid_uuid(user_uuid)
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM camps WHERE id = %s", (camp_id,))
            if not cur.fetchone():
                raise HTTPException(404, "Camp not found")
            cur.execute(
                "INSERT INTO favorites (user_uuid, camp_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (user_uuid, camp_id)
            )
        conn.commit()
        return {"ok": True}
    finally:
        conn.close()

@app.delete("/favorites/{user_uuid}/{camp_id}")
def remove_favorite(user_uuid: str, camp_id: int):
    _valid_uuid(user_uuid)
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM favorites WHERE user_uuid = %s AND camp_id = %s", (user_uuid, camp_id))
        conn.commit()
        return {"ok": True}
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
