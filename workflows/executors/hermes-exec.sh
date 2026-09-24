#!/usr/bin/env bash
# hermes-exec.sh — ponte mínima AIOX → Hermes (External Executor pattern)
# Segue o contrato de .aiox-core/development/external-executors/README.md:
#   AIOX mantém a orquestração; Hermes executa; artefatos ficam em .aiox/external-runs/
#
# Uso:
#   hermes-exec.sh -t <slug> -f <prompt_file> [-d workdir] [-m model]
#   hermes-exec.sh -t <slug> -p "prompt inline" [-d workdir]
#
# Saída (key=value, mesmo formato do aiox-delegate):
#   STATUS=started|finished|failed
#   RUN_DIR, OUTPUT, PROMPT, COMMAND, EXIT_CODE
set -euo pipefail

SLUG=""; PROMPT=""; PROMPT_FILE=""; WORKDIR=""; MODEL=""
RUN_BASE=".aiox/external-runs"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -t|--task) SLUG="$2"; shift 2 ;;
    -f|--prompt-file) PROMPT_FILE="$2"; shift 2 ;;
    -p|--prompt) PROMPT="$2"; shift 2 ;;
    -d|--workdir) WORKDIR="$2"; shift 2 ;;
    -m|--model) MODEL="$2"; shift 2 ;;
    -r|--run-dir) RUN_BASE="$2"; shift 2 ;;
    -h|--help) grep '^#' "$0" | head -12; exit 0 ;;
    *) echo "ERRO: argumento desconhecido $1" >&2; exit 64 ;;
  esac
done

[[ -z "$SLUG" ]] && { echo "ERRO: -t <slug> é obrigatório" >&2; exit 64; }
if [[ -z "$PROMPT" && -z "$PROMPT_FILE" ]]; then
  echo "ERRO: -f <prompt_file> ou -p <prompt> é obrigatório" >&2; exit 64
fi
[[ -z "$WORKDIR" ]] && WORKDIR="$(pwd)"

# Hermes: instalação por usuário quando acessível; senão a do root.
# O usuário 'hermes' não lê /root/* (home 700) — nesse caso use a do root.
if [[ -x "/home/hermes/.local/bin/hermes" ]] && sudo -u hermes test -r "$WORKDIR" 2>/dev/null; then
  HERMES=(sudo -u hermes /home/hermes/.local/bin/hermes)
elif [[ -x "/root/.local/bin/hermes" ]]; then
  HERMES=(/root/.local/bin/hermes)
elif [[ -x "$HOME/.local/bin/hermes" ]]; then
  HERMES=("$HOME/.local/bin/hermes")
else
  echo "ERRO: hermes não encontrado em ~/.local/bin" >&2; exit 69
fi

TS="$(date +%Y%m%d-%H%M%S)"
RUN_DIR="$RUN_BASE/$TS-$SLUG"
mkdir -p "$RUN_DIR"

if [[ -n "$PROMPT_FILE" ]]; then
  cp "$PROMPT_FILE" "$RUN_DIR/prompt.md"
else
  printf '%s\n' "$PROMPT" > "$RUN_DIR/prompt.md"
fi

ARGS=(-z "$(cat "$RUN_DIR/prompt.md")" --in "$WORKDIR" --usage-file "$RUN_DIR/usage.json")
[[ -n "$MODEL" ]] && ARGS+=(-m "$MODEL")
printf '%q ' "${HERMES[@]}" "${ARGS[@]}" > "$RUN_DIR/command.txt"

echo "STATUS=started"
echo "RUN_DIR=$RUN_DIR"
echo "PROMPT=$RUN_DIR/prompt.md"
echo "COMMAND=$(cat "$RUN_DIR/command.txt")"

set +e
"${HERMES[@]}" "${ARGS[@]}" > "$RUN_DIR/output.md" 2> "$RUN_DIR/hermes.log"
EXIT_CODE=$?
set -e

cat > "$RUN_DIR/metadata.json" <<EOF
{
  "provider": "hermes",
  "slug": "$SLUG",
  "workdir": "$WORKDIR",
  "exit_code": $EXIT_CODE,
  "finished_at": "$(date -Is)"
}
EOF

echo "OUTPUT=$RUN_DIR/output.md"
echo "EXIT_CODE=$EXIT_CODE"
if [[ $EXIT_CODE -eq 0 ]]; then
  echo "STATUS=finished"
else
  echo "STATUS=failed"
fi
exit $EXIT_CODE
