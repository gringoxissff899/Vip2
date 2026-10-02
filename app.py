import os
import sqlite3
from pathlib import Path
from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "change-this-secret-before-production")
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")
ACCESS_KEY = os.environ.get("ACCESS_KEY", "GRINGOZIN803")
DB_PATH = Path(os.environ.get("GRINGOZIN_DB", "gringozin.sqlite3"))
DEFAULTS = {
    "BYPASSV1": True,
    "HS_NECK": False,
    "HS_CHEST": False,
    "BACKJUMPV1": True,
    "HIGH_SENSI": True,
    "ZIG_ZAG_MOVE": True,
}


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE IF NOT EXISTS settings (feature TEXT PRIMARY KEY, value INTEGER NOT NULL)")
    for feature, value in DEFAULTS.items():
        conn.execute("INSERT OR IGNORE INTO settings(feature, value) VALUES (?, ?)", (feature, int(value)))
    conn.commit()
    return conn


def get_config():
    conn = db()
    rows = conn.execute("SELECT feature, value FROM settings").fetchall()
    conn.close()
    return {row["feature"]: bool(row["value"]) for row in rows}


def client_ip():
    forwarded = request.headers.get("X-Forwarded-For", "")
    return forwarded.split(",")[0].strip() or request.remote_addr or "indisponível"


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/login")
def login():
    body = request.get_json(silent=True) or {}
    if body.get("key", "").strip() != ACCESS_KEY:
        return jsonify({"success": False, "error": "Chave incorreta ou inválida!"}), 401
    session["authenticated"] = True
    return jsonify({"success": True})


@app.get("/api/status")
def status():
    if not session.get("authenticated"):
        return jsonify({"error": "Não autenticado"}), 401
    return jsonify({"status": "online", "ip": client_ip(), "config": get_config()})


@app.post("/api/toggle")
def toggle():
    if not session.get("authenticated"):
        return jsonify({"error": "Não autenticado"}), 401
    body = request.get_json(silent=True) or {}
    feature, value = body.get("feature"), body.get("value")
    if feature not in DEFAULTS or not isinstance(value, bool):
        return jsonify({"success": False, "error": "Função ou valor inválido"}), 400
    conn = db()
    conn.execute("UPDATE settings SET value = ? WHERE feature = ?", (int(value), feature))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "feature": feature, "value": value, "ip": client_ip()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
