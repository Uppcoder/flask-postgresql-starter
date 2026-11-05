"""A small Flask app on PostgreSQL: a notes API.

The database comes from DATABASE_URL (postgresql://user:password@host:5432/db),
which Uppcoder sets when the app is connected to PostgreSQL and docker compose
sets locally. The table is created on startup, so a fresh database just works.

Uppcoder starts the app as `python app.py` and expects it on 127.0.0.1, port 8000;
HOST and PORT change that (docker compose sets HOST=0.0.0.0).
"""
import os

import psycopg
from flask import Flask, abort, jsonify, request

DATABASE_URL = os.environ.get("DATABASE_URL", "")

app = Flask(__name__)


def connect():
    if not DATABASE_URL:
        abort(503, "DATABASE_URL is not set: connect the app to PostgreSQL")
    return psycopg.connect(DATABASE_URL)


def create_table():
    if DATABASE_URL:
        with psycopg.connect(DATABASE_URL) as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS notes ("
                " id SERIAL PRIMARY KEY,"
                " text TEXT NOT NULL,"
                " created_at TIMESTAMPTZ NOT NULL DEFAULT now())"
            )


@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(503)
def error(e):
    return jsonify({"error": e.description}), e.code


@app.get("/")
def index():
    return {
        "app": "Flask + PostgreSQL starter",
        "database": "connected" if DATABASE_URL else "not connected (DATABASE_URL is not set)",
        "try": ["GET /notes", "POST /notes {\"text\": \"...\"}", "GET /health"],
    }


@app.get("/health")
def health():
    with connect() as conn:
        version = conn.execute("SELECT version()").fetchone()[0]
    return {"ok": True, "postgres": version.split(",")[0]}


@app.get("/notes")
def list_notes():
    with connect() as conn:
        rows = conn.execute("SELECT id, text, created_at FROM notes ORDER BY id").fetchall()
    return jsonify([{"id": r[0], "text": r[1], "created_at": r[2].isoformat()} for r in rows])


@app.post("/notes")
def add_note():
    text = str((request.get_json(silent=True) or {}).get("text", "")).strip()
    if not text:
        abort(400, "text must not be empty")
    with connect() as conn:
        row = conn.execute(
            "INSERT INTO notes (text) VALUES (%s) RETURNING id, created_at", (text,)
        ).fetchone()
    return {"id": row[0], "text": text, "created_at": row[1].isoformat()}, 201


@app.delete("/notes/<int:note_id>")
def delete_note(note_id):
    with connect() as conn:
        if conn.execute("DELETE FROM notes WHERE id = %s", (note_id,)).rowcount == 0:
            abort(404, "no such note")
    return "", 204


create_table()

if __name__ == "__main__":
    app.run(
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "8000")),
        debug=os.environ.get("FLASK_DEBUG") == "1",
    )
