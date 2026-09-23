"""Fila de trabalhos (SQLite) + worker que executa os jobs.

Dois tipos de job:
  agente            → dispara `kimi -p ... --auto` como sub-processo (etapas de copy/design)
  video_higgsfield  → chamada direta à API Higgsfield (geradores.py)
"""
import json
import os
import sqlite3
import threading
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "dados", "painel.db")
LOGS = os.path.join(ROOT, "logs", "trabalhos")
ESTADOS = ("fila", "rodando", "concluido", "erro")

_worker = None
_lock = threading.Lock()

def _conn():
    c = sqlite3.connect(DB, timeout=30)
    c.row_factory = sqlite3.Row
    return c

def init():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    os.makedirs(LOGS, exist_ok=True)
    with _conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS jobs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT, tipo TEXT, estado TEXT DEFAULT 'fila',
            criado REAL, atualizado REAL, log_path TEXT, meta TEXT DEFAULT '{}')""")
        # recuperação de jobs interrompidos por queda do servidor
        c.execute("UPDATE jobs SET estado='fila', atualizado=? WHERE estado='rodando'", (time.time(),))

def criar_job(produto, tipo, meta=None):
    agora = time.time()
    with _conn() as c:
        cur = c.execute(
            "INSERT INTO jobs(produto,tipo,estado,criado,atualizado,log_path,meta) VALUES(?,?,?,?,?,?,?)",
            (produto, tipo, "fila", agora, agora, "", json.dumps(meta or {}, ensure_ascii=False)))
        jid = cur.lastrowid
        log_path = os.path.join(LOGS, f"{jid}.log")
        c.execute("UPDATE jobs SET log_path=? WHERE id=?", (log_path, jid))
    return jid

def obter_job(jid):
    with _conn() as c:
        return c.execute("SELECT * FROM jobs WHERE id=?", (jid,)).fetchone()

def listar_jobs(produto=None, limite=50):
    with _conn() as c:
        if produto:
            rows = c.execute("SELECT * FROM jobs WHERE produto=? ORDER BY id DESC LIMIT ?",
                             (produto, limite)).fetchall()
        else:
            rows = c.execute("SELECT * FROM jobs ORDER BY id DESC LIMIT ?", (limite,)).fetchall()
    return rows

def _marcar(jid, estado, meta=None):
    with _conn() as c:
        if meta is not None:
            c.execute("UPDATE jobs SET estado=?, atualizado=?, meta=? WHERE id=?",
                      (estado, time.time(), json.dumps(meta, ensure_ascii=False), jid))
        else:
            c.execute("UPDATE jobs SET estado=?, atualizado=? WHERE id=?", (estado, time.time(), jid))

def _executar(job):
    from . import etapas
    meta = json.loads(job["meta"] or "{}")
    log_path = job["log_path"]
    with open(log_path, "a", encoding="utf-8") as logf:
        logf.write(f"== job {job['id']} | {job['tipo']} | produto={job['produto']} | {time.strftime('%H:%M:%S')} ==\n")
        logf.flush()
        try:
            etapas.executar(job["tipo"], meta, logf)
            meta.pop("erro", None)
            _marcar(job["id"], "concluido", meta)
            logf.write("\n== CONCLUIDO ==\n")
        except Exception as e:
            meta["erro"] = str(e)[:500]
            _marcar(job["id"], "erro", meta)
            logf.write(f"\n== ERRO: {e} ==\n")

def _loop():
    while True:
        try:
            with _conn() as c:
                row = c.execute("SELECT * FROM jobs WHERE estado='fila' ORDER BY id LIMIT 1").fetchone()
            if row:
                _marcar(row["id"], "rodando")
                _executar(row)
            else:
                time.sleep(2)
        except Exception:
            time.sleep(5)

def arrancar_worker():
    global _worker
    with _lock:
        if _worker is None or not _worker.is_alive():
            init()
            _worker = threading.Thread(target=_loop, daemon=True, name="painel-worker")
            _worker.start()

def ler_log(jid, linhas=200):
    job = obter_job(jid)
    if not job or not job["log_path"] or not os.path.exists(job["log_path"]):
        return ""
    with open(job["log_path"], encoding="utf-8", errors="replace") as f:
        return "".join(f.readlines()[-linhas:])
