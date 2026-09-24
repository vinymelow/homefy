#!/usr/bin/env bash
# hermes-exec.sh — ponte AIOX → Hermes (External Executor pattern)
# Segue o contrato de .aiox-core/development/external-executors/README.md:
#   AIOX mantém a orquestração; Hermes executa; artefatos ficam em .aiox/external-runs/
#
# Uso:
#   hermes-exec.sh -t <slug> -f <prompt_file> [-d workdir] [-m model] [-T timeout]
#   hermes-exec.sh -t <slug> -p "prompt inline" [-d workdir]
#
# Saída (key=value, mesmo formato do aiox-delegate):
#   STATUS=started|finished|failed|timeout|rejected
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

SLUG=""; PROMPT=""; PROMPT_FILE=""; WORKDIR=""; MODEL=""; TIMEOUT_MIN=""
RUN_BASE=".aiox/external-runs"
DEFAULT_TIMEOUT_MIN=20

while [[ $# -gt 0 ]]; do
  case "$1" in
    -t|--task) SLUG="$2"; shift 2 ;;
    -f|--prompt-file) PROMPT_FILE="$2"; shift 2 ;;
    -p|--prompt) PROMPT="$2"; shift 2 ;;
    -d|--workdir) WORKDIR="$2"; shift 2 ;;
    -m|--model) MODEL="$2"; shift 2 ;;
    -T|--timeout) TIMEOUT_MIN="$2"; shift 2 ;;
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

# Pré-checks (status REJECTED) -----------------------------------------------
if [[ ! -d "$WORKDIR" ]]; then
  echo "STATUS=rejected"; echo "REASON=workdir-not-found: $WORKDIR"; exit 65
fi
if [[ ! -r "$WORKDIR" ]]; then
  echo "STATUS=rejected"; echo "REASON=workdir-not-readable: $WORKDIR"; exit 65
fi
if [[ -n "$PROMPT_FILE" && ! -r "$PROMPT_FILE" ]]; then
  echo "STATUS=rejected"; echo "REASON=prompt-file-not-readable: $PROMPT_FILE"; exit 65
fi

# Hermes: instalação por usuário quando acessível; senão a do root.
# O usuário 'hermes' não lê /root/* (home 700) — nesse caso use a do root.
HERMES=()
if [[ -x "/home/hermes/.local/bin/hermes" ]] && sudo -u hermes test -r "$WORKDIR" 2>/dev/null; then
  HERMES=(sudo -u hermes /home/hermes/.local/bin/hermes)
elif [[ -x "/root/.local/bin/hermes" ]]; then
  HERMES=(/root/.local/bin/hermes)
elif [[ -x "$HOME/.local/bin/hermes" ]]; then
  HERMES=("$HOME/.local/bin/hermes")
else
  echo "STATUS=rejected"; echo "REASON=hermes-binary-not-found"; exit 69
fi

TS="$(date +%Y%m%d-%H%M%S)"
RUN_DIR="$RUN_BASE/$TS-$SLUG"
mkdir -p "$RUN_DIR/artifacts"

if [[ -n "$PROMPT_FILE" ]]; then
  cp "$PROMPT_FILE" "$RUN_DIR/prompt.md"
else
  printf '%s\n' "$PROMPT" > "$RUN_DIR/prompt.md"
fi

# Prompt vazio = REJECTED
if [[ ! -s "$RUN_DIR/prompt.md" ]]; then
  echo "STATUS=rejected"; echo "REASON=empty-prompt"; echo "RUN_DIR=$RUN_DIR"; exit 65
fi

STARTED_AT="$(date -Is)"
ARGS=(-z "$(cat "$RUN_DIR/prompt.md")" --in "$WORKDIR" --usage-file "$RUN_DIR/usage.json")
[[ -n "$MODEL" ]] && ARGS+=(-m "$MODEL")
printf '%q ' "${HERMES[@]}" "${ARGS[@]}" > "$RUN_DIR/command.txt"

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
  FATAL_PATTERNS='^(HTTP [45][0-9][0-9]:)|does not exist or you do not have access|(Invalid API key)|(Traceback \(most recent call last\))|(Connection refused)|(NameResolutionError)'
  if grep -qE "$FATAL_PATTERNS" "$RUN_DIR/output.md" "$RUN_DIR/hermes.log" 2>/dev/null; then
    STATUS="failed"
  elif [[ ! -s "$RUN_DIR/output.md" ]]; then
    STATUS="partial"
  fi
fi

FINISHED_AT="$(date -Is)"
OUTPUT_BYTES=0; [[ -s "$RUN_DIR/output.md" ]] && OUTPUT_BYTES=$(wc -c < "$RUN_DIR/output.md")

# result.json — resultado estruturado (Fase 11) -------------------------------
python3 - "$RUN_DIR" "$SLUG" "$WORKDIR" "$STATUS" "$EXIT_CODE" "$STARTED_AT" "$FINISHED_AT" "$OUTPUT_BYTES" ${MODEL:+"$MODEL"} <<'PYEOF'
import json, sys, os
run_dir, slug, workdir, status, exit_code, started, finished, out_bytes = sys.argv[1:9]
model = sys.argv[9] if len(sys.argv) > 9 else None
usage = None
if os.path.exists(os.path.join(run_dir, "usage.json")):
    try:
        usage = json.load(open(os.path.join(run_dir, "usage.json")))
    except Exception:
        usage = None
result = {
    "run_id": os.path.basename(run_dir),
    "task": slug,
    "status": status.upper(),
    "started_at": started,
    "finished_at": finished,
    "exit_code": int(exit_code),
    "model": model,
    "workdir": workdir,
    "artifacts": {
        "output": f"{run_dir}/output.md",
        "log": f"{run_dir}/hermes.log",
        "usage": f"{run_dir}/usage.json" if usage is not None else None,
        "dir": f"{run_dir}/artifacts",
    },
    "output_bytes": int(out_bytes),
    "usage": usage,
}
json.dump(result, open(os.path.join(run_dir, "result.json"), "w"), indent=2)
PYEOF

# metadata.json — backward compat --------------------------------------------
cat > "$RUN_DIR/metadata.json" <<EOF
{
  "provider": "hermes",
  "slug": "$SLUG",
  "workdir": "$WORKDIR",
  "status": "$STATUS",
  "exit_code": $EXIT_CODE,
  "started_at": "$STARTED_AT",
  "finished_at": "$FINISHED_AT",
  "output_bytes": $OUTPUT_BYTES
}
EOF

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
