from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import sys
import os

# Thêm đường dẫn import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.core.scorer import calculate_quality_score
from backend.core.models import TrajectoryCheckRequest, QualityResponse
import sqlite3
import json
from datetime import datetime

app = FastAPI(title="Axis Data Quality Bot", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====================== SERVE FRONTEND ======================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    index_path = os.path.join(BASE_DIR, "frontend", "index.html")
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse("<h1>Frontend chưa được deploy đúng. Kiểm tra lại thư mục frontend/</h1>", status_code=500)

# ====================== API ======================
def get_db():
    db_path = os.path.join(BASE_DIR, "axis_quality.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.post("/check", response_model=QualityResponse)
async def check_quality(request: TrajectoryCheckRequest):
    score, issues, metrics = calculate_quality_score(request.trajectory, request.mode)
    
    conn = get_db()
    conn.execute("""
        INSERT INTO checks (timestamp, filename, score, issues, mode)
        VALUES (?, ?, ?, ?, ?)
    """, (datetime.now().isoformat(), request.filename, score, json.dumps(issues), request.mode))
    conn.commit()
    conn.close()

    return QualityResponse(
        score=score,
        issues=issues,
        metrics=metrics,
        timestamp=datetime.now().isoformat()
    )

@app.get("/history")
async def get_history(limit: int = 20):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM checks ORDER BY timestamp DESC LIMIT ?", 
        (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.on_event("startup")
async def startup_event():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS checks (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            filename TEXT,
            score REAL,
            issues TEXT,
            mode TEXT
        )
    """)
    conn.commit()
    conn.close()