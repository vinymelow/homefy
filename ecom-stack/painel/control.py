"""Estado do cockpit: identidade, sessões, chat, runs, aprovações e auditoria."""
from __future__ import annotations

import json
import os
import sqlite3
import time
from . import security, settings


def conn():
    c = sqlite3.connect(settings.DB_PATH, timeout=30)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA foreign_keys=ON")
    return c


def init():
    with conn() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS admins(
          id INTEGER PRIMARY KEY CHECK(id=1), email TEXT UNIQUE NOT NULL,
          password_hash TEXT NOT NULL, totp_secret TEXT NOT NULL,
          totp_enabled INTEGER NOT NULL DEFAULT 0, created_at REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS web_sessions(
          token_hash TEXT PRIMARY KEY, admin_id INTEGER NOT NULL, csrf TEXT NOT NULL,
          created_at REAL NOT NULL, expires_at REAL NOT NULL,
          FOREIGN KEY(admin_id) REFERENCES admins(id) ON DELETE CASCADE);
        CREATE TABLE IF NOT EXISTS recovery_codes(
          code_hash TEXT PRIMARY KEY, admin_id INTEGER NOT NULL, used_at REAL,
          FOREIGN KEY(admin_id) REFERENCES admins(id) ON DELETE CASCADE);
        CREATE TABLE IF NOT EXISTS chat_sessions(
          id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, product TEXT,
          hermes_session_id TEXT, created_at REAL NOT NULL, updated_at REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS messages(
          id INTEGER PRIMARY KEY AUTOINCREMENT, session_id INTEGER NOT NULL,
          role TEXT NOT NULL CHECK(role IN ('user','assistant','system')),
          content TEXT NOT NULL, job_id INTEGER, created_at REAL NOT NULL,
          FOREIGN KEY(session_id) REFERENCES chat_sessions(id) ON DELETE CASCADE);
        CREATE TABLE IF NOT EXISTS workflow_runs(
          id INTEGER PRIMARY KEY AUTOINCREMENT, workflow TEXT NOT NULL, product TEXT NOT NULL,
          status TEXT NOT NULL, current_step TEXT, created_at REAL NOT NULL,
          updated_at REAL NOT NULL, cost_usd REAL NOT NULL DEFAULT 0, error TEXT);
        CREATE TABLE IF NOT EXISTS approvals(
          id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT NOT NULL, target TEXT NOT NULL,
          impact TEXT NOT NULL, cost_estimate TEXT, payload TEXT NOT NULL DEFAULT '{}',
          status TEXT NOT NULL DEFAULT 'pending', created_at REAL NOT NULL,
          expires_at REAL NOT NULL, decided_at REAL, decision_note TEXT);
        CREATE TABLE IF NOT EXISTS audit_events(
          id INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT NOT NULL, actor TEXT NOT NULL,
          detail TEXT NOT NULL, created_at REAL NOT NULL);
        """)
    ensure_bootstrap_token()


def has_admin() -> bool:
    with conn() as c:
        return c.execute("SELECT 1 FROM admins LIMIT 1").fetchone() is not None


def ensure_bootstrap_token():
    if has_admin() or settings.BOOTSTRAP_FILE.exists():
        return
    token = security.new_secret(32)
    settings.BOOTSTRAP_FILE.write_text(token, encoding="utf-8")
    os.chmod(settings.BOOTSTRAP_FILE, 0o600)


def valid_bootstrap(token: str) -> bool:
    try:
        expected = settings.BOOTSTRAP_FILE.read_text(encoding="utf-8").strip()
    except OSError:
        return False
    return bool(token) and security.token_hash(token) == security.token_hash(expected)


def create_admin(email: str, password: str, token: str):
    if has_admin() or not valid_bootstrap(token):
        raise ValueError("Inicialização indisponível ou token inválido")
    secret = security.new_totp_secret()
    with conn() as c:
        c.execute("INSERT INTO admins(id,email,password_hash,totp_secret,created_at) VALUES(1,?,?,?,?)",
                  (email.lower().strip(), security.hash_password(password), secret, time.time()))
    audit("admin.created", "bootstrap", {"email": email.lower().strip()})
    return secret


def verify_login(email: str, password: str, code: str):
    with conn() as c:
        row = c.execute("SELECT * FROM admins WHERE email=?", (email.lower().strip(),)).fetchone()
        if not row or not security.verify_password(password, row["password_hash"]):
            return None
        if row["totp_enabled"] and not security.verify_totp(row["totp_secret"], code):
            recovery = security.token_hash(code.strip().upper())
            hit = c.execute("SELECT 1 FROM recovery_codes WHERE code_hash=? AND used_at IS NULL", (recovery,)).fetchone()
            if not hit:
                return None
            c.execute("UPDATE recovery_codes SET used_at=? WHERE code_hash=?", (time.time(), recovery))
        return row


def create_session(admin_id: int = 1):
    token, csrf = security.new_secret(), security.new_secret(18)
    now = time.time()
    with conn() as c:
        c.execute("DELETE FROM web_sessions WHERE expires_at<?", (now,))
        c.execute("INSERT INTO web_sessions VALUES(?,?,?,?,?)",
                  (security.token_hash(token), admin_id, csrf, now, now + settings.SESSION_TTL))
    return token, csrf


def get_session(token: str | None):
    if not token:
        return None
    with conn() as c:
        return c.execute("SELECT s.*,a.email FROM web_sessions s JOIN admins a ON a.id=s.admin_id WHERE token_hash=? AND expires_at>?",
                         (security.token_hash(token), time.time())).fetchone()


def delete_session(token: str | None):
    if token:
        with conn() as c:
            c.execute("DELETE FROM web_sessions WHERE token_hash=?", (security.token_hash(token),))


def enable_totp(admin_id: int, code: str):
    with conn() as c:
        row = c.execute("SELECT totp_secret FROM admins WHERE id=?", (admin_id,)).fetchone()
        if not row or not security.verify_totp(row[0], code):
            return []
        codes = [security.new_secret(9).upper() for _ in range(8)]
        c.execute("UPDATE admins SET totp_enabled=1 WHERE id=?", (admin_id,))
        c.executemany("INSERT INTO recovery_codes(code_hash,admin_id) VALUES(?,?)",
                      [(security.token_hash(value), admin_id) for value in codes])
    audit("admin.totp_enabled", "admin", {})
    return codes


def audit(kind: str, actor: str, detail):
    safe = json.dumps(detail, ensure_ascii=False)[:4000]
    with conn() as c:
        c.execute("INSERT INTO audit_events(kind,actor,detail,created_at) VALUES(?,?,?,?)",
                  (kind, actor, safe, time.time()))


def recent_audit(limit=30):
    with conn() as c:
        return c.execute("SELECT * FROM audit_events ORDER BY id DESC LIMIT ?", (limit,)).fetchall()


def new_chat(title: str, product: str | None = None):
    now = time.time()
    with conn() as c:
        cur = c.execute("INSERT INTO chat_sessions(title,product,created_at,updated_at) VALUES(?,?,?,?)",
                        (title[:120], product or None, now, now))
        return cur.lastrowid


def chats():
    with conn() as c:
        return c.execute("SELECT * FROM chat_sessions ORDER BY updated_at DESC").fetchall()


def chat(chat_id: int):
    with conn() as c:
        room = c.execute("SELECT * FROM chat_sessions WHERE id=?", (chat_id,)).fetchone()
        msgs = c.execute("SELECT * FROM messages WHERE session_id=? ORDER BY id", (chat_id,)).fetchall()
        return room, msgs


def add_message(chat_id: int, role: str, content: str, job_id=None):
    now = time.time()
    with conn() as c:
        c.execute("INSERT INTO messages(session_id,role,content,job_id,created_at) VALUES(?,?,?,?,?)",
                  (chat_id, role, content, job_id, now))
        c.execute("UPDATE chat_sessions SET updated_at=? WHERE id=?", (now, chat_id))


def approvals(status="pending"):
    with conn() as c:
        return c.execute("SELECT * FROM approvals WHERE status=? ORDER BY id DESC", (status,)).fetchall()

def create_approval(action: str, target: str, impact: str, cost_estimate: str | None, payload: dict, ttl=3600):
    now = time.time()
    with conn() as c:
        cur = c.execute("INSERT INTO approvals(action,target,impact,cost_estimate,payload,created_at,expires_at) VALUES(?,?,?,?,?,?,?)",
                        (action, target, impact, cost_estimate, json.dumps(payload, ensure_ascii=False), now, now + ttl))
        aid = cur.lastrowid
    audit("approval.created", "admin", {"id": aid, "action": action, "target": target})
    return aid

def get_approval(aid: int):
    with conn() as c:
        return c.execute("SELECT * FROM approvals WHERE id=?", (aid,)).fetchone()


def decide_approval(aid: int, decision: str, note: str):
    if decision not in ("approved", "rejected"):
        raise ValueError("decisão inválida")
    with conn() as c:
        row = c.execute("SELECT * FROM approvals WHERE id=? AND status='pending' AND expires_at>?", (aid, time.time())).fetchone()
        if not row:
            return False
        c.execute("UPDATE approvals SET status=?,decided_at=?,decision_note=? WHERE id=?",
                  (decision, time.time(), note[:500], aid))
    audit("approval.decided", "admin", {"id": aid, "decision": decision})
    return True
