#!/usr/bin/env bash
# hermes-exec.sh — ponte AIOX → Hermes (External Executor pattern)
# Segue o contrato de .aiox-core/development/external-executors/README.md:
#   AIOX mantém a orquestração; Hermes executa; artefatos ficam em .aiox/external-runs/
#
# Uso:
#   hermes-exec.sh -t <slug> -f <prompt_file> [-d workdir] [-m model] [-T timeout] [--toolsets list]
#   hermes-exec.sh -t <slug> -p "prompt inline" [-d workdir]
#
# Toolsets: default conservador "terminal,file" (Fase 36 — small
# context + progressive disclosure). O toolset "skills" e o schema completo
# de tools do Hermes excedem o limite de payload do provider Groq desta conta;
# sobrecarregue com --toolsets "a,b,c" quando a task precisar de mais
# (ex.: --toolsets "terminal,file,web") e com consciência do rate limit.
#
# Saída (key=value, mesmo formato do aiox-delegate):
#   STATUS=started|success|partial|failed|timeout|rejected
#   RUN_DIR, OUTPUT, PROMPT, COMMAND, EXIT_CODE, RESULT_JSON
#
# Contrato de status (Fase 11):
#   SUCCESS  — exit 0, saída não vazia, sem padrões fatais detectados
#   PARTIAL  — exit 0 mas saída vazia/curta demais (revisão humana necessária)
#   FAILED   — exit != 0 OU padrão fatal detectado na saída/log (ex.: HTTP 404 de modelo)
#   TIMEOUT  — excedeu o timeout (-T, default 20min, alinhado com modelGovernance)
#   REJECTED — pré-checks falharam (workdir ilegível, prompt vazio, hermes ausente)
#
# Artefatos por run:
#   prompt.md command.txt output.md hermes.log usage.json result.json metadata.json
set -euo pipefail

SLUG=""; PROMPT=""; PROMPT_FILE=""; WORKDIR=""; MODEL=""; TIMEOUT_MIN=""; TOOLSETS=""
RUN_BASE=".aiox/external-runs"
DEFAULT_TIMEOUT_MIN=20
DEFAULT_TOOLSETS="terminal,file"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -t|--task) SLUG="$2"; shift 2 ;;
    -f|--prompt-file) PROMPT_FILE="$2"; shift 2 ;;
    -p|--prompt) PROMPT="$2"; shift 2 ;;
    -d|--workdir) WORKDIR="$2"; shift 2 ;;
    -m|--model) MODEL="$2"; shift 2 ;;
    -T|--timeout) TIMEOUT_MIN="$2"; shift 2 ;;
    -u|--toolsets) TOOLSETS="$2"; shift 2 ;;
    -r|--run-dir) RUN_BASE="$2"; shift 2 ;;
    -h|--help) grep '^#' "$0" | head -20; exit 0 ;;
    *) echo "ERRO: argumento desconhecido $1" >&2; exit 64 ;;
  esac
done

[[ -z "$SLUG" ]] && { echo "ERRO: -t <slug> é obrigatório" >&2; exit 64; }
if [[ -z "$PROMPT" && -z "$PROMPT_FILE" ]]; then
  echo "ERRO: -f <prompt_file> ou -p <prompt> é obrigatório" >&2; exit 64
fi
[[ -z "$WORKDIR" ]] && WORKDIR="$(pwd)"
[[ -z "$TIMEOUT_MIN" ]] && TIMEOUT_MIN="$DEFAULT_TIMEOUT_MIN"
[[ -z "$TOOLSETS" ]] && TOOLSETS="$DEFAULT_TOOLSETS"

if [[ ! "$SLUG" =~ ^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$ ]]; then
  echo "STATUS=rejected"; echo "REASON=invalid-task-slug"; exit 65
fi
if [[ ! "$TIMEOUT_MIN" =~ ^[1-9][0-9]*$ ]] || (( TIMEOUT_MIN > 1440 )); then
  echo "STATUS=rejected"; echo "REASON=invalid-timeout-minutes"; exit 65
fi
if [[ ! "$TOOLSETS" =~ ^[A-Za-z0-9_-]+(,[A-Za-z0-9_-]+)*$ ]]; then
  echo "STATUS=rejected"; echo "REASON=invalid-toolsets"; exit 65
fi

if [[ "$RUN_BASE" != /* ]]; then
  if [[ -d "$WORKDIR" ]]; then
    RUN_BASE="$WORKDIR/$RUN_BASE"
  else
    RUN_BASE="$(pwd)/$RUN_BASE"
  fi
fi
TS="$(date -u +%Y%m%d-%H%M%S)"
RUN_DIR="$RUN_BASE/$TS-$$-$SLUG"
mkdir -p "$RUN_BASE"
mkdir "$RUN_DIR"
mkdir "$RUN_DIR/artifacts"
touch "$RUN_DIR/output.md" "$RUN_DIR/hermes.log"
STARTED_AT="$(date -Is)"

write_result() {
  local result_status="$1" result_exit="$2" result_reason="${3:-}"
  local finished_at output_bytes
  finished_at="$(date -Is)"
  output_bytes="$(wc -c < "$RUN_DIR/output.md")"
  python3 - "$RUN_DIR" "$SLUG" "$WORKDIR" "$result_status" "$result_exit" \
    "$STARTED_AT" "$finished_at" "$output_bytes" "$TOOLSETS" "$MODEL" "$result_reason" <<'PYEOF'
import json, sys, os
run_dir, slug, workdir, status, exit_code, started, finished, out_bytes = sys.argv[1:9]
toolsets, model, reason = sys.argv[9:12]
usage = None
usage_path = os.path.join(run_dir, "usage.json")
if os.path.exists(usage_path):
    try:
        with open(usage_path, encoding="utf-8") as handle:
            usage = json.load(handle)
    except (OSError, ValueError):
        usage = None
artifact_dir = os.path.join(run_dir, "artifacts")
artifact_files = sorted(
    os.path.join(artifact_dir, name)
    for name in os.listdir(artifact_dir)
    if os.path.isfile(os.path.join(artifact_dir, name))
)
result = {
    "run_id": os.path.basename(run_dir),
    "task": slug,
    "status": status.upper(),
    "reason": reason or None,
    "started_at": started,
    "finished_at": finished,
    "exit_code": int(exit_code),
    "model": model or None,
    "toolsets": toolsets,
    "workdir": workdir,
    "artifacts": {
        "output": os.path.join(run_dir, "output.md"),
        "log": os.path.join(run_dir, "hermes.log"),
        "usage": usage_path if usage is not None else None,
        "dir": artifact_dir,
        "files": artifact_files,
    },
    "output_bytes": int(out_bytes),
    "usage": usage,
}
with open(os.path.join(run_dir, "result.json"), "w", encoding="utf-8") as handle:
    json.dump(result, handle, indent=2, ensure_ascii=False)
metadata = {
    "provider": "hermes", "slug": slug, "workdir": workdir,
    "status": status, "exit_code": int(exit_code), "toolsets": toolsets,
    "started_at": started, "finished_at": finished,
    "output_bytes": int(out_bytes), "reason": reason or None,
}
with open(os.path.join(run_dir, "metadata.json"), "w", encoding="utf-8") as handle:
    json.dump(metadata, handle, indent=2, ensure_ascii=False)
PYEOF
}

reject_run() {
  local reason="$1" code="${2:-65}"
  printf '%s\n' "$reason" > "$RUN_DIR/hermes.log"
  write_result rejected "$code" "$reason"
  echo "RUN_DIR=$RUN_DIR"
  echo "OUTPUT=$RUN_DIR/output.md"
  echo "RESULT_JSON=$RUN_DIR/result.json"
  echo "EXIT_CODE=$code"
  echo "STATUS=rejected"
  echo "REASON=$reason"
  exit "$code"
}

# Pré-checks (status REJECTED + result.json) ---------------------------------
[[ -d "$WORKDIR" ]] || reject_run "workdir-not-found" 65
[[ -r "$WORKDIR" ]] || reject_run "workdir-not-readable" 65
if [[ -n "$PROMPT_FILE" && ! -r "$PROMPT_FILE" ]]; then
  reject_run "prompt-file-not-readable" 65
fi

# Hermes: instalação por usuário quando acessível; senão a do root.
# O usuário 'hermes' não lê /root/* (home 700) — nesse caso use a do root.
HERMES=()
HERMES_RUN_USER=""
if [[ -x "/home/hermes/.local/bin/hermes" ]] && sudo -u hermes test -r "$WORKDIR" 2>/dev/null; then
  HERMES=(sudo -u hermes /home/hermes/.local/bin/hermes)
  HERMES_RUN_USER="hermes"
elif [[ -x "/root/.local/bin/hermes" ]]; then
  HERMES=(/root/.local/bin/hermes)
elif [[ -x "$HOME/.local/bin/hermes" ]]; then
  HERMES=("$HOME/.local/bin/hermes")
else
  reject_run "hermes-binary-not-found" 69
fi

if [[ -n "$PROMPT_FILE" ]]; then
  cp "$PROMPT_FILE" "$RUN_DIR/prompt.md"
else
  printf '%s\n' "$PROMPT" > "$RUN_DIR/prompt.md"
fi

# Prompt vazio = REJECTED
if [[ ! -s "$RUN_DIR/prompt.md" ]]; then
  reject_run "empty-prompt" 65
fi

# O processo Hermes precisa escrever usage.json diretamente. Quando a execução
# usa o usuário dedicado, o diretório recém-criado do run é entregue a ele.
if [[ -n "$HERMES_RUN_USER" ]]; then
  chown -R "$HERMES_RUN_USER:$HERMES_RUN_USER" "$RUN_DIR"
fi

ARGS=(-z "$(cat "$RUN_DIR/prompt.md")" --in "$WORKDIR" --usage-file "$RUN_DIR/usage.json" -t "$TOOLSETS")
[[ -n "$MODEL" ]] && ARGS+=(-m "$MODEL")
printf '%q ' "${HERMES[@]}" -z "<prompt-from:$RUN_DIR/prompt.md>" --in "$WORKDIR" \
  --usage-file "$RUN_DIR/usage.json" -t "$TOOLSETS" > "$RUN_DIR/command.txt"
[[ -n "$MODEL" ]] && printf '%q ' -m "$MODEL" >> "$RUN_DIR/command.txt"
printf '\n' >> "$RUN_DIR/command.txt"

echo "STATUS=started"
echo "RUN_DIR=$RUN_DIR"
echo "PROMPT=$RUN_DIR/prompt.md"
echo "COMMAND=$(cat "$RUN_DIR/command.txt")"

# Execução com timeout --------------------------------------------------------
set +e
timeout --signal=TERM "${TIMEOUT_MIN}m" "${HERMES[@]}" "${ARGS[@]}" \
  > "$RUN_DIR/output.md" 2> "$RUN_DIR/hermes.log"
EXIT_CODE=$?
set -e

STATUS="success"
if [[ $EXIT_CODE -eq 124 ]]; then
  STATUS="timeout"
elif [[ $EXIT_CODE -ne 0 ]]; then
  STATUS="failed"
else
  # Hermes pode sair 0 mesmo com erro fatal (ex.: HTTP 404 de modelo).
  # Detecta padrões fatais na saída/log e downgrade de SUCCESS → FAILED.
  FATAL_PATTERNS='^(HTTP [45][0-9][0-9]:)|does not exist or you do not have access|(Invalid API key)|(Traceback \(most recent call last\))|(Connection refused)|(NameResolutionError)|(payload too large)|^(Request payload too large)|(API call failed)|(can.t reach the model provider)'
  USAGE_FAILED="false"
  if [[ -s "$RUN_DIR/usage.json" ]]; then
    USAGE_FAILED="$(python3 - "$RUN_DIR/usage.json" <<'PYEOF'
import json, sys
try:
    with open(sys.argv[1], encoding="utf-8") as handle:
        print("true" if json.load(handle).get("failed") is True else "false")
except (OSError, ValueError):
    print("false")
PYEOF
)"
  fi
  if [[ "$USAGE_FAILED" == "true" ]] || grep -qiE "$FATAL_PATTERNS" "$RUN_DIR/output.md" "$RUN_DIR/hermes.log" 2>/dev/null; then
    STATUS="failed"
  elif [[ ! -s "$RUN_DIR/output.md" ]] || (( $(wc -c < "$RUN_DIR/output.md") < 40 )); then
    STATUS="partial"
  fi
fi

# result.json — resultado estruturado (Fase 11) -------------------------------
write_result "$STATUS" "$EXIT_CODE"

echo "OUTPUT=$RUN_DIR/output.md"
echo "RESULT_JSON=$RUN_DIR/result.json"
echo "EXIT_CODE=$EXIT_CODE"
echo "STATUS=$STATUS"

case "$STATUS" in
  success) exit 0 ;;
  partial) exit 0 ;;   # revisão humana; orquestrador decide
  timeout) exit 124 ;;
  *)       exit 1 ;;
esac
