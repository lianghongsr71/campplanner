"""
Summer Camp Finder - FastAPI Backend
GET /camps: age, q (keyword), category filters. Admin: X-Admin-Key for POST/PUT/DELETE.
Sessions: GET /camps/{id}/sessions, POST/PUT/DELETE (admin).
Favorites: GET /favorites/{uuid} returns session+camp info,
           POST /favorites/{uuid} body={session_id or camp_id},
           DELETE /favorites/{uuid}/{fav_id}.
"""
from typing import Optional, List
import re
from decimal import Decimal
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Query, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Summer Camp Finder API")

# ── Pydantic models ──────────────────────────────────────────────────────────

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
    image_url: Optional[str] = None
    tag: Optional[str] = None

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

class SessionCreate(BaseModel):
    week_number: int
    label: Optional[str] = None
    start_date: str
    end_date: str
    price_per_week: Optional[float] = None

class SessionUpdate(BaseModel):
    week_number: Optional[int] = None
    label: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    price_per_week: Optional[float] = None

class FavoriteAdd(BaseModel):
    camp_id: int
    session_id: Optional[int] = None  # None = no specific session (legacy / single-date camp)

# ── Auth ─────────────────────────────────────────────────────────────────────

def require_admin(x_admin_key: Optional[str] = Header(None, alias="X-Admin-Key")):
    # Auth temporarily disabled - re-enable when ADMIN_API_KEY is configured
    pass

# ── Middleware ────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── DB helpers ────────────────────────────────────────────────────────────────

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

def _row_to_dict(row) -> dict:
    d = dict(row)
    for k, v in list(d.items()):
        if hasattr(v, "isoformat"):
            d[k] = v.isoformat()
        elif isinstance(v, Decimal):
            d[k] = float(v)
    return d

_CAMP_COLS = (
    "id, name, organization, age_min, age_max, start_date, end_date, "
    "time_start, time_end, price, category, address, latitude, longitude, "
    "registration_link, days_of_week, description, image_url, tag"
)

# ── Root / health ─────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "Summer Camp Finder API", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/admin/ping")
def admin_ping(_: bool = Depends(require_admin)):
    return {"ok": True}

# ── Camps ─────────────────────────────────────────────────────────────────────

@app.get("/camps")
@app.get("/camps/")
def list_camps(
    age: Optional[int] = Query(None),
    q: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    limit: Optional[int] = Query(None),
):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            conditions, params = [], []
            if age is not None:
                conditions.append("age_min <= %s AND age_max >= %s")
                params.extend([age, age])
            if (q or "").strip():
                p = "%" + q.strip() + "%"
                conditions.append("(name ILIKE %s OR organization ILIKE %s OR category ILIKE %s OR address ILIKE %s OR description ILIKE %s)")
                params.extend([p] * 5)
            if (category or "").strip():
                conditions.append("category ILIKE %s")
                params.append("%" + category.strip() + "%")
            where = " AND ".join(conditions) if conditions else "TRUE"
            sql = f"SELECT {_CAMP_COLS} FROM camps WHERE {where} ORDER BY name"
            if limit:
                sql += f" LIMIT {int(limit)}"
            cur.execute(sql, tuple(params))
            rows = cur.fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        conn.close()

@app.get("/camps/{camp_id}")
def get_camp(camp_id: int):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT {_CAMP_COLS} FROM camps WHERE id = %s", (camp_id,))
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
            cur.execute(
                f"""INSERT INTO camps (name, organization, age_min, age_max, start_date, end_date,
                    time_start, time_end, price, category, address, latitude, longitude,
                    registration_link, days_of_week, description, image_url, tag)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                RETURNING {_CAMP_COLS}""",
                (body.name, body.organization, body.age_min, body.age_max,
                 body.start_date or None, body.end_date or None,
                 body.time_start, body.time_end, body.price, body.category,
                 body.address, body.latitude, body.longitude, body.registration_link,
                 body.days_of_week, body.description, body.image_url, body.tag)
            )
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
            cur.execute(
                """UPDATE camps SET
                    name=COALESCE(%s,name), organization=COALESCE(%s,organization),
                    age_min=COALESCE(%s,age_min), age_max=COALESCE(%s,age_max),
                    start_date=COALESCE(%s,start_date), end_date=COALESCE(%s,end_date),
                    time_start=COALESCE(%s,time_start), time_end=COALESCE(%s,time_end),
                    price=COALESCE(%s,price), category=COALESCE(%s,category),
                    address=COALESCE(%s,address), latitude=COALESCE(%s,latitude),
                    longitude=COALESCE(%s,longitude), registration_link=COALESCE(%s,registration_link),
                    days_of_week=COALESCE(%s,days_of_week), description=COALESCE(%s,description),
                    image_url=COALESCE(%s,image_url), tag=COALESCE(%s,tag)
                WHERE id=%s""",
                (body.name, body.organization, body.age_min, body.age_max,
                 body.start_date, body.end_date, body.time_start, body.time_end,
                 float(body.price) if body.price is not None else None,
                 body.category, body.address, body.latitude, body.longitude,
                 body.registration_link, body.days_of_week, body.description,
                 body.image_url, body.tag, camp_id)
            )
            cur.execute(f"SELECT {_CAMP_COLS} FROM camps WHERE id = %s", (camp_id,))
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

# ── Sessions ──────────────────────────────────────────────────────────────────

@app.get("/camps/{camp_id}/sessions")
def list_sessions(camp_id: int):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM camps WHERE id = %s", (camp_id,))
            if not cur.fetchone():
                raise HTTPException(404, "Camp not found")
            cur.execute(
                "SELECT id, camp_id, week_number, label, start_date, end_date, price_per_week "
                "FROM camp_sessions WHERE camp_id = %s ORDER BY week_number",
                (camp_id,)
            )
            rows = cur.fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        conn.close()

@app.post("/camps/{camp_id}/sessions")
def create_session(camp_id: int, body: SessionCreate, _: bool = Depends(require_admin)):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM camps WHERE id = %s", (camp_id,))
            if not cur.fetchone():
                raise HTTPException(404, "Camp not found")
            cur.execute(
                """INSERT INTO camp_sessions (camp_id, week_number, label, start_date, end_date, price_per_week)
                VALUES (%s,%s,%s,%s,%s,%s)
                ON CONFLICT (camp_id, week_number) DO UPDATE SET
                    label=EXCLUDED.label, start_date=EXCLUDED.start_date,
                    end_date=EXCLUDED.end_date, price_per_week=EXCLUDED.price_per_week
                RETURNING id, camp_id, week_number, label, start_date, end_date, price_per_week""",
                (camp_id, body.week_number, body.label, body.start_date, body.end_date, body.price_per_week)
            )
            row = cur.fetchone()
        conn.commit()
        return _row_to_dict(row)
    finally:
        conn.close()

@app.put("/sessions/{session_id}")
def update_session(session_id: int, body: SessionUpdate, _: bool = Depends(require_admin)):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE camp_sessions SET
                    week_number=COALESCE(%s,week_number), label=COALESCE(%s,label),
                    start_date=COALESCE(%s,start_date), end_date=COALESCE(%s,end_date),
                    price_per_week=COALESCE(%s,price_per_week)
                WHERE id=%s
                RETURNING id, camp_id, week_number, label, start_date, end_date, price_per_week""",
                (body.week_number, body.label, body.start_date, body.end_date,
                 body.price_per_week, session_id)
            )
            row = cur.fetchone()
        if not row:
            raise HTTPException(404, "Session not found")
        conn.commit()
        return _row_to_dict(row)
    finally:
        conn.close()

@app.delete("/sessions/{session_id}")
def delete_session(session_id: int, _: bool = Depends(require_admin)):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM camp_sessions WHERE id = %s RETURNING id", (session_id,))
            if not cur.fetchone():
                raise HTTPException(404, "Session not found")
        conn.commit()
        return {"ok": True}
    finally:
        conn.close()

# ── Favorites ─────────────────────────────────────────────────────────────────

_UUID_RE = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)

def _valid_uuid(user_uuid: str):
    if not _UUID_RE.match(user_uuid):
        raise HTTPException(400, "Invalid user UUID")

@app.get("/favorites/{user_uuid}")
def get_favorites(user_uuid: str):
    """Returns list of favorited items with full camp + session info."""
    _valid_uuid(user_uuid)
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    f.fav_id,
                    f.camp_id,
                    f.session_id,
                    c.name, c.organization, c.age_min, c.age_max,
                    c.time_start, c.time_end, c.price,
                    c.category, c.address, c.registration_link,
                    c.days_of_week, c.description, c.image_url, c.tag,
                    c.latitude, c.longitude,
                    COALESCE(s.start_date, c.start_date) AS start_date,
                    COALESCE(s.end_date,   c.end_date)   AS end_date,
                    COALESCE(s.price_per_week, c.price)  AS price_per_week,
                    s.week_number,
                    s.label AS session_label
                FROM favorites f
                JOIN camps c ON f.camp_id = c.id
                LEFT JOIN camp_sessions s ON f.session_id = s.id
                WHERE f.user_uuid = %s
                ORDER BY f.created_at
            """, (user_uuid,))
            rows = cur.fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        conn.close()

@app.get("/favorites/{user_uuid}/camp_ids")
def get_favorite_camp_ids(user_uuid: str):
    """Returns distinct camp_ids that the user has any favorite for (for heart-button state)."""
    _valid_uuid(user_uuid)
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT DISTINCT camp_id FROM favorites WHERE user_uuid = %s",
                (user_uuid,)
            )
            rows = cur.fetchall()
        return [r["camp_id"] for r in rows]
    finally:
        conn.close()

@app.post("/favorites/{user_uuid}")
def add_favorite(user_uuid: str, body: FavoriteAdd):
    """Add a favorite. body = {camp_id, session_id (optional)}."""
    _valid_uuid(user_uuid)
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM camps WHERE id = %s", (body.camp_id,))
            if not cur.fetchone():
                raise HTTPException(404, "Camp not found")
            if body.session_id is not None:
                cur.execute("SELECT id FROM camp_sessions WHERE id = %s AND camp_id = %s",
                            (body.session_id, body.camp_id))
                if not cur.fetchone():
                    raise HTTPException(404, "Session not found for this camp")
            cur.execute(
                """INSERT INTO favorites (user_uuid, camp_id, session_id)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
                RETURNING fav_id""",
                (user_uuid, body.camp_id, body.session_id)
            )
            row = cur.fetchone()
        conn.commit()
        return {"ok": True, "fav_id": row["fav_id"] if row else None}
    finally:
        conn.close()

@app.delete("/favorites/{user_uuid}/{fav_id}")
def remove_favorite(user_uuid: str, fav_id: int):
    """Remove a specific favorite by fav_id."""
    _valid_uuid(user_uuid)
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM favorites WHERE user_uuid = %s AND fav_id = %s RETURNING fav_id",
                (user_uuid, fav_id)
            )
            if not cur.fetchone():
                raise HTTPException(404, "Favorite not found")
        conn.commit()
        return {"ok": True}
    finally:
        conn.close()

@app.delete("/favorites/{user_uuid}/camp/{camp_id}")
def remove_favorite_by_camp(user_uuid: str, camp_id: int):
    """Remove ALL favorites for a camp (used when toggling heart off)."""
    _valid_uuid(user_uuid)
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM favorites WHERE user_uuid = %s AND camp_id = %s",
                (user_uuid, camp_id)
            )
        conn.commit()
        return {"ok": True}
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
