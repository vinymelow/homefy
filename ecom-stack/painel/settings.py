"""Configuração central do painel Homefy, sem carregar segredos no Git."""
from pathlib import Path
import os

ECOM_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ECOM_ROOT.parent
STATE_DIR = Path(os.environ.get("HOMEFY_STATE_DIR", ECOM_ROOT / "dados"))
LOG_DIR = Path(os.environ.get("HOMEFY_LOG_DIR", ECOM_ROOT / "logs"))
ASSET_DIR = Path(os.environ.get("HOMEFY_ASSET_DIR", ECOM_ROOT / "assets"))
DB_PATH = STATE_DIR / "painel.db"
RUNS_DIR = STATE_DIR / "runs"
BOOTSTRAP_FILE = STATE_DIR / "bootstrap-token"

PUBLIC_ORIGIN = os.environ.get("HOMEFY_PUBLIC_ORIGIN", "http://127.0.0.1:8787").rstrip("/")
COOKIE_SECURE = os.environ.get("HOMEFY_COOKIE_SECURE", "0") == "1"
SESSION_TTL = int(os.environ.get("HOMEFY_SESSION_TTL", str(12 * 3600)))
HERMES_MODEL = os.environ.get("HOMEFY_HERMES_MODEL", "")
HERMES_PROVIDER = os.environ.get("HOMEFY_HERMES_PROVIDER", "")
HERMES_REASONING = os.environ.get("HOMEFY_HERMES_REASONING", "low")
HERMES_TIMEOUT_MIN = int(os.environ.get("HOMEFY_HERMES_TIMEOUT_MIN", "20"))
MAX_DAILY_RUNS = int(os.environ.get("HOMEFY_MAX_DAILY_RUNS", "30"))
ECOM_ENV_FILE = Path(os.environ.get("ECOM_ENV_FILE", ECOM_ROOT / "config" / ".env"))

for directory in (STATE_DIR, LOG_DIR, ASSET_DIR, RUNS_DIR):
    directory.mkdir(parents=True, exist_ok=True)
